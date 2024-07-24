import json

def load_test_data(file_name):
    with open(file_name, 'r') as f:
        return json.load(f)

def colorize(text, color):
    colors = {
        'pink': '\033[95m',
        'blue': '\033[94m',
        'green': '\033[92m',
        'cyan': '\033[96m',
        'end': '\033[0m'
    }
    return f"{colors[color]}{text}{colors['end']}"

def administer_test(test_data, test_name):
    print(f"\n{'='*40}\n{test_name.upper()}\n{'='*40}\n")
    questions = test_data[test_name]['questions']
    answers = []
    for i, question in enumerate(questions, 1):
        print(f"\n{colorize(f'Question {i}:', 'blue')}\n{colorize(question['question'], 'cyan')}\n")
        for j, option in enumerate(question['options'], 1):
            print(f"{j}. {colorize(option, 'pink')}")
        answer = input(f"\n{colorize('Enter the number of your answer: ', 'green')}")
        answers.append(int(answer) - 1)  # assuming you want to store the index of the answer
    return answers

def calculate_score(test_data, test_name, answers):
    questions = test_data[test_name]['questions']
    score = 0
    for i, answer in enumerate(answers):
        score += answer + 1
    return score

def determine_result(test_data, test_name, score):
    metrics = test_data[test_name]['metrics']
    for metric, description in metrics.items():
        min_score, max_score = map(int, metric.split('-'))
        if min_score <= score <= max_score:
            return description
    return 'Unknown result'

def main():
    file_name = 'psychiatric_tests.json'
    test_data = load_test_data(file_name)
    print("Select a test:")
    for i, test_name in enumerate(test_data.keys()):
        print(f"{i+1}. {test_name}")
    choice = int(input("Enter the number of your choice: "))
    test_name = list(test_data.keys())[choice - 1]
    answers = administer_test(test_data, test_name)
    score = calculate_score(test_data, test_name, answers)
    result = determine_result(test_data, test_name, score)

    print("\n" + "="*40)
    print(f"  {test_name.upper()} TEST RESULTS  ")
    print("="*40)
    print(f"\nYour score is: {score}")
    print(f"Criteria: {test_data[test_name]['criteria']}")
    print(f"\n{colorize('Your result:', 'blue')}\n{result}\n")
    print("="*40)

if __name__ == "__main__":
    main()