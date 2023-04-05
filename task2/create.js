db.jeopardy.insertOne({
    showNumber: 42,
    airDate: "2023-01-01",
    round: "Jeopardy!",
    category: "HISTORY",
    value: "$1000000",
    question: "Who is the founder of Moscow?",
    answer: "Yuri I Vladimirovich a.k.a. Long Arm"
})


db.jeopardy.insertMany([
    {
        showNumber: 228,
        airDate: "2021-07-14",
        round: "Jeopardy!",
        category: "3-LETTER WORDS",
        value: "$1000000",
        question: "Frozen water",
        answer: "ice"
    },
    {
        showNumber: 1337,
        airDate: "496-03-17",
        round: "Jeopardy!",
        category: "CELEBS",
        value: "$1000000",
        question: "Who recorded track Stan",
        answer: "Eminem"
    }
])
