import unittest
from app import create_app, db
from app.models import User, Product
from config import TestConfig
import datetime

class BasicTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_app_exists(self):
        self.assertFalse(self.app is None)
        self.assertTrue(self.app.config['TESTING'])

    def test_user_model(self):
        u = User(username='testuser', email='test@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()
        self.assertTrue(u.id is not None)
        self.assertTrue(u.check_password('password123'))
        self.assertFalse(u.check_password('wrongpassword'))

    def test_product_model(self):
        p = Product(name='Test Product', description='A product for testing', price=9.99, stock=10)
        db.session.add(p)
        db.session.commit()
        self.assertTrue(p.id is not None)
        self.assertEqual(p.name, 'Test Product')
        self.assertTrue(isinstance(p.created_at, datetime.datetime))

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(TestConfig)
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

        # Create a test user
        u = User(username='testuser', email='test@example.com')
        u.set_password('password123')
        db.session.add(u)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def login(self, username, password):
        return self.client.post('/auth/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.client.get('/auth/logout', follow_redirects=True)

    def test_login_logout(self):
        # Test login
        response = self.login('testuser', 'password123')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Hi, testuser!', response.data) # Check for dashboard welcome

        # Test logout
        response = self.logout()
        self.assertEqual(response.status_code, 200)
        # After logout, it should redirect to login page (or main page showing login link)
        self.assertIn(b'Sign In', response.data) # Assuming base.html shows "Sign In" when logged out

    def test_login_invalid_credentials(self):
        response = self.login('testuser', 'wrongpassword')
        self.assertEqual(response.status_code, 200) # Stays on login page
        self.assertIn(b'Invalid username or password', response.data)

    def test_dashboard_access_unauthenticated(self):
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Sign In', response.data) # Should redirect to login

    def test_dashboard_access_authenticated(self):
        self.login('testuser', 'password123')
        response = self.client.get('/', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data) # Main dashboard heading
        self.assertIn(b'Products', response.data) # Product table heading
        self.assertIn(b'Product Stock Levels', response.data) # Chart heading

if __name__ == '__main__':
    unittest.main()
