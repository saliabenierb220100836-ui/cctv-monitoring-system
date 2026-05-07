from app import create_app

app = create_app()

with app.app_context():
    from app import db
    from app.models.user import User
    try:
        # --- ADD THIS LINE TEMPORARILY ---
        db.drop_all() 
        
        # Now create the new structure
        db.create_all() 
        
        if not User.query.filter_by(username='felicity').first():
            admin = User(username='felicity')
            admin.set_password('bernabe')
            db.session.add(admin)
            db.session.commit()
            print("<h1>SUCCESS</h1><p>Database wiped and recreated. User 'felicity' created.</p>")
        else:
            print("<h1>NOTICE</h1><p>Setup already complete.</p>")
    except Exception as e:
        print(f"<h1>ERROR</h1><p>{str(e)}</p>")