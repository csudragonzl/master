from job_web.app import create_app

app = create_app('development')
app.jinja_env.filters['zip'] = zip
if __name__ == '__main__':
    app.run(debug=True)
