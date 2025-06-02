from flask import render_template, request, redirect, url_for, jsonify # Add jsonify
from flask_login import login_required, current_user
from app.main import bp
from app.models import Product, User
from app.main.forms import SearchForm
from app import db
import json # To pass data to template safely

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    search_form = SearchForm()
    page = request.args.get('page', 1, type=int)

    query = Product.query

    search_term_get = request.args.get('search', None, type=str) # Get search term from GET args first

    if search_form.validate_on_submit(): # Handles POST from search form
        search_term_post = search_form.search_term.data
        # Redirect to GET with search term to make URL bookmarkable
        return redirect(url_for('main.index', search=search_term_post if search_term_post else None, page=1))

    if search_term_get:
        search_form.search_term.data = search_term_get # Populate form for display
        query = query.filter(Product.name.ilike(f'%{search_term_get}%'))

    products_pagination = query.order_by(Product.name.asc()).paginate(
        page, per_page=5, error_out=False)

    products_for_table = products_pagination.items

    # Data for chart: Get all products (or filter if needed, but for simplicity all for now)
    # For a real app, you might want to limit this or aggregate differently
    all_products_for_chart = Product.query.order_by(Product.stock.desc()).limit(10).all() # Top 10 by stock
    chart_labels = [p.name for p in all_products_for_chart]
    chart_data = [p.stock for p in all_products_for_chart]

    return render_template('index.html', title='Dashboard',
                           search_form=search_form, products=products_for_table,
                           pagination=products_pagination, current_search=search_term_get,
                           chart_labels=json.dumps(chart_labels), # Use json.dumps for safety
                           chart_data=json.dumps(chart_data))
