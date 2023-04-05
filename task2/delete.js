db.jeopardy.deleteMany({showNumber: {$lt: 1000}})
printjson(db.jeopardy.find({showNumber: 42}))
