let adjectives = [ "Beautiful", "Witty", "Wicked", "Confusing", "Rich", "New", "Strange", "Rocky", "Circular", "Helpful",
    "Competent" , "Smelly", "Stable", "Grumpy", "Devoted", "Smart", "Muscular", "Graceful", "Scary", "Safe",
    "Wooden", "Sleepy", "Tardy", "Hungry", "Strange", "Hopeful", "Proud", "Dainty", "Royal", "Arrogant",
    "Round", "Efficient", "Youthful", "Cumbersome", "Fickle", "Mild", "Expensive", "Small", "Rude", "Generous", "Courageous",
    "Zany", "Thin", "Round", "Oval", "Dark", "Hot", "Modern", "Petite", "Weary"
    ]
let nouns = [
    "Teacher", "Doctor", "Chef", "Student", "Pilot", "Firefighter", "Lawyer", "Mechanic", "Engineer", "Farmer",
    "Cat", "Dog", "Horse", "Bird", "Fish", "Snake", "Rabbit", "Elephant", "Squirrel", "Fox",
    "Human", "Dog", "Way", "Art", "World", "Information", "Map", "Family", "Government", "Health", "System",
    "Computer", "Meat","Year", "Music", "Person", "Book", "Item", "Information", "Car", "Law", "Bird",
    "Literature", "Problem", "Software", "Control", "Knowledge", "Power", "Ability", "Economics", "Love", "Internet",
    "Television", "Science", "Library", "Nature", "Earth", "Fact", "Idea", "Bus", "Investment", "Area", "Society",
    "Activity", "Story", "Industry", "Media", "Organization", "Technology", "House"
]

const randomItem = (arr) => {
    return arr[Math.floor(Math.random() * arr.length)];
}

document.getElementById("generate-button").addEventListener('click', function(event) {
    const codeNameInput = document.getElementById("code-name")
    codeNameInput.value = `${randomItem(adjectives)} ${randomItem(nouns)}`
})

