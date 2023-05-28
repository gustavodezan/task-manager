db.createUser(
    {
        user: "admin",
        pwd: "senha",
        roles: [
            {
                role: "readWrite",
                db: "taskmanager"
            }
        ]
    }
)