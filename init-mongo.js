db = db.getSiblingDB('mongo_database');

db.createUser(
    {
        user: "mongo_admin",
        pwd: "mongo_admin_password",
        roles: [
            {
                role: "readWrite",
                db: "mongo_database"
            }
        ]
    }
);

quit()