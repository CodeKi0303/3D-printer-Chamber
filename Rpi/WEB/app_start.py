from Backend import app

if __name__ == "__main__":
	ip = '0.0.0.0'
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.run(host=ip, debug=True)
