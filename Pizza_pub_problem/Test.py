from itertools import permutations

class StudentTransporter:
    def __init__(self,ce_students, ds_students):
        self.ce_students = ce_students
        self.ds_students = ds_students
        self.possible_solutions = []

    def is_valid_solution(self, solution):
        ce_count, ds_count = 0, 0
        for group in solution:
            ce_count += group.count('CE')
            ds_count += group.count('DS')
            if ds_count > ce_count:
                return False
        return True

    def generate_solutions(self):
        students = ['CE'] * self.ce_students + ['DS'] * self.ds_students
        all_permutations = permutations(students)

        for permutation in all_permutations:
            permutation = list(permutation)  # Convert tuple to list
            solution = []
            for _ in range(len(permutation) // 2):
                solution.append([permutation.pop(), permutation.pop()])
            if self.is_valid_solution(solution):
                self.possible_solutions.append(solution)

    def list_possible_solutions(self):
        self.generate_solutions()
        if not self.possible_solutions:
            print("No valid solutions.")
        else:
            for i, solution in enumerate(self.possible_solutions):
                print(f"Solution {i + 1}: {solution}")

# Example usage
ce_students = 12  # Number of CE students
ds_students = 11  # Number of DS students

transporter = StudentTransporter(ce_students, ds_students)
transporter.list_possible_solutions()