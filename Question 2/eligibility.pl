:- use_module(library(csv)).         % For CSV handling
:- use_module(library(http/http_server)).  % For REST API
:- use_module(library(http/http_dispatch)). 
:- use_module(library(http/http_json)). 
:- use_module(library(http/http_parameters)).

% Load CSV data into the knowledge base
load_csv_data(File) :-
    csv_read_file(File, Rows, [functor(student), arity(4)]),
    maplist(assert, Rows).

% Rules for eligibility
eligible_for_scholarship(Student_ID, Name, Attendance, CGPA) :-
    student(Student_ID, Name, Attendance, CGPA),
    Attendance >= 75,
    CGPA >= 9.0.

permitted_for_exam(Student_ID, Name, Attendance, CGPA) :-
    student(Student_ID, Name, Attendance, CGPA),
    Attendance >= 75.

% CORS middleware: Add CORS headers to each response
add_cors_headers :-
    format('Access-Control-Allow-Origin: *~n'),
    format('Access-Control-Allow-Methods: GET, POST, OPTIONS~n'),
    format('Access-Control-Allow-Headers: Content-Type~n').

% REST API Handlers
:- http_handler(root(scholarship), check_scholarship, []).
:- http_handler(root(exam), check_exam_permission, []).

% API to check scholarship eligibility
check_scholarship(Request) :-
    add_cors_headers,
    http_parameters(Request, [student_id(StudentID, [atom])]),
    (   atom_number(StudentID, StudentIDInt),  % Convert the atom to an integer
        eligible_for_scholarship(StudentIDInt, Name, Attendance, CGPA) ->  
        reply_json_dict(_{
            status: "Eligible",
            student_id: StudentIDInt,
            name: Name,
            attendance: Attendance,
            cgpa: CGPA
        })
    ;   atom_number(StudentID, StudentIDInt),
        student(StudentIDInt, Name, Attendance, CGPA) ->  
        reply_json_dict(_{
            status: "Not Eligible",
            student_id: StudentIDInt,
            name: Name,
            attendance: Attendance,
            cgpa: CGPA
        })
    ;   reply_json_dict(_{status: "Not Found", message: "Student not found."})
    ).


% API to check exam permission
check_exam_permission(Request) :-
    add_cors_headers,
    http_parameters(Request, [student_id(StudentID, [atom])]),
    (   atom_number(StudentID, StudentIDInt),  % Convert student ID to integer
        student(StudentIDInt, Name, Attendance, CGPA) ->  % Check if student exists
        (   Attendance >= 75 ->  % Check if attendance is >= 75
            reply_json_dict(_{
                status: "Permitted",
                student_id: StudentIDInt,
                name: Name,
                attendance: Attendance,
                cgpa: CGPA
            })
        ;   reply_json_dict(_{
                status: "Not Permitted",
                student_id: StudentIDInt,
                name: Name,
                attendance: Attendance,
                cgpa: CGPA
            })
        )
    ;   reply_json_dict(_{status: "Not Found", message: "Student not found."})
    ).


% Start server
start_server(Port) :-
    http_server(http_dispatch, [port(Port)]).