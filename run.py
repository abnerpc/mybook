from mybook import mybookapp

app = mybookapp.create_app()
app.run(debug=True, use_reloader=True)
