db.jeopardy.updateOne({showNumber: 42, airDate: "2023-01-01"}, {$set: {value: "$2000000"}})
db.jeopardy.replaceOne(
    {
        showNumber: 228,
        airDate: "2021-07-14"
    },
    {
        showNumber: 282,
        airDate: "2027-01-19",
        round: "Double Jeopardy!",
        category: "BE FRUITFUL & MULTIPLY",
        value: "$2000000",
        question: "3123412 x 848293",
        answer: "2649568535716"
    }
)
printjson(db.jeopardy.find({value: "$2000000"}))
