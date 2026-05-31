// Application Database 및 유저 생성
db = db.getSiblingDB('myapp');

db.createUser({
    user: process.env.APP_DB_USERNAME,
    pwd: process.env.APP_DB_PASSWORD,
    roles: [
        { role: "readWrite", db: "myapp" }
    ]
});

// 샘플 컬렉션 생성
db.createCollection("users");
db.users.createIndex({ "email": 1 }, { unique: true });

// 읽기 전용 유저 생성
db.createUser({
    user: "readonly",
    pwd: "readonly_password",
    roles: [
        { role: "read", db: "myapp" }
    ]
});
