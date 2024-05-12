import random
import sys

from flask import Flask, render_template, request

import scripts.query_profs as qp

app = Flask(__name__)
course_searcher = qp.ProfQuery(files_path="ubc-pair-grade-data/tableau-dashboard*/**/**/*.csv")


@app.route('/')
def index():
    return render_template('./index.html')


@app.route('/get_courses', methods=['POST'])
def retrieve_data():
    # print(request.form.get())
    query: str = request.form.get('prof')
    opening = query.find('(')
    prof = query[0:opening - 1]
    # print(prof)

    # print(course_searcher.query(prof))
    return [course.__dict__() for course in course_searcher.query(prof)]


@app.route('/search', methods=['GET'])
def search_prof() -> dict[str, list[dict[str, int | str]]]:
    query = request.args.get('term')
    # print(request.args)

    if query is not None and query != "":
        query_results = course_searcher.close_profs(query, count=10)
        courses_results = [course_searcher.query(prof) for prof in query_results]

        response = {'results': []}

        i = 1  # id required for format
        for prof, courses in zip(query_results, courses_results):
            subjects_taught: dict[str, int] = {}
            for course in courses:
                if course.subject in subjects_taught:
                    subjects_taught[course.subject] += 1
                else:
                    subjects_taught.update({course.subject: 1})
            subjects_taught = {k: v for k, v in sorted(subjects_taught.items(), key=lambda x: x[1], reverse=True)}
            most_popular_subjects: list[str] = list(subjects_taught.keys())[0:min(len(subjects_taught), 3)]

            field = f'{prof} ('

            j = 0
            while j < len(most_popular_subjects):
                if j == len(most_popular_subjects) - 1:
                    field += f'{most_popular_subjects[j]})'
                else:
                    field += f'{most_popular_subjects[j]}, '

                j += 1

            response['results'].append({"id": random.randint(0, sys.maxsize), "text": field})

            i += 1

        return response
    else:
        return {'results': []}  # return empty if query is empty


if __name__ == '__main__':
    app.run()
