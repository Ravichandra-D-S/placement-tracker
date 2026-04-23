daily_plan = {
    1: "Variables + Data Types",
    2: "Operators",
    3: "If Else",
    4: "Loops",
    5: "Strings",
    6: "Lists",
    7: "Revision"
}

daily_questions = {
    1: [
        {"q": "Sum of two numbers", "link": "https://leetcode.com/problems/two-sum/"},
        {"q": "Palindrome Number", "link": "https://leetcode.com/problems/palindrome-number/"}
    ],
    2: [
        {"q": "Power of Two", "link": "https://leetcode.com/problems/power-of-two/"},
        {"q": "Reverse Integer", "link": "https://leetcode.com/problems/reverse-integer/"}
    ]
}

for i in range(8, 91):
    daily_plan[i] = "DSA Practice"
    daily_questions[i] = [
        {"q": "Practice problem", "link": "https://leetcode.com/"}
    ]