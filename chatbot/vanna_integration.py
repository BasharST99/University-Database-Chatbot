from vanna.openai import OpenAI_Chat
from vanna.chromadb import ChromaDB_VectorStore
import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)

vn = MyVanna(config={
    'api_key': os.getenv('OPENAI_API_KEY'),
    'model': 'gpt-3.5-turbo'
})

def train_vanna():
    # Load and train the DDL (schema)
    ddl = open("schema.sql", encoding="utf-8").read()
    vn.train(ddl=ddl)
    
    # Add semantic explanations of relationships
    relationship_explanations = [
        # English explanations
        ("The students table contains all student information including their names, majors, departments and GPAs.",
         "Each student has a unique student_id that links to their enrollments."),
         
        ("Professors teach courses and belong to departments.",
         "The professors table connects to courses through the professor_id foreign key."),
         
        ("Courses are taught by professors and students enroll in them.",
         "The enrollments table connects students to courses through student_id and course_id."),
         
        ("A student's department represents their primary field of study.",
         "This is different from a professor's department which is where they teach."),
         
        # Arabic explanations
        ("جدول الطلاب يحتوي على معلومات جميع الطلاب بما في ذلك أسماؤهم وتخصصاتهم وأقسامهم ومعدلاتهم.",
         "كل طالب لديه معرف فريد (student_id) يرتبط بتسجيلاته في المواد."),
         
        ("الأساتذة يدرسون المواد وينتمون إلى أقسام.",
         "جدول الأساتذة متصل بجدول المواد من خلال المفتاح الأجنبي professor_id."),
         
        ("المواد يدرسها الأساتذة ويسجل فيها الطلاب.",
         "جدول التسجيلات يربط الطلاب بالمواد من خلال student_id و course_id."),
         
        ("قسم الطالب يمثل مجال دراسته الرئيسي.",
         "هذا يختلف عن قسم الأستاذ الذي يمثل مكان تدريسه.")
    ]
    
    for explanation in relationship_explanations:
        vn.train(documentation=explanation[0])
        if len(explanation) > 1:
            vn.train(documentation=explanation[1])

    # Business logic explanations
    business_rules = [
        # English
        "When calculating average GPA, we always use the students table.",
        "Course enrollment information comes from joining students, enrollments and courses tables.",
        "A professor's department is where they teach, while a student's department is their field of study.",
        "To find which students take a course, join students with enrollments and courses.",
        
        # Arabic
        "عند حساب المعدل التراكمي المتوسط، نستخدم دائماً جدول الطلاب.",
        "معلومات تسجيل المادة تأتي من ربط جداول الطلاب والتسجيلات والمواد.",
        "قسم الأستاذ هو مكان تدريسه بينما قسم الطالب هو مجال دراسته.",
        "للعثور على الطلاب المسجلين في مادة ما، اربط جدول الطلاب مع التسجيلات والمواد."
    ]
    
    for rule in business_rules:
        vn.train(documentation=rule)

    # Natural language examples
    qna_examples = [
        # English
        ("How do I find which students are in the Computer Science department?",
         "Query the students table filtering by department = 'Computer Science'"),
         
        ("How can I see which courses a student is taking?",
         "Join the students table with enrollments and courses tables using the student_id and course_id relationships"),
         
        ("What's the relationship between professors and courses?",
         "Each course has a professor_id that links to the professors table"),
         
        # Arabic
        ("كيف يمكنني معرفة الطلاب في قسم علوم الحاسوب؟",
         "استعلام جدول الطلاب مع التصفية حسب القسم = 'علوم الحاسوب'"),
         
        ("كيف أرى المواد التي يأخذها طالب معين؟",
         "اربط جدول الطلاب مع جداول التسجيلات والمواد باستخدام العلاقات student_id و course_id")
    ]
    
    for question, answer in qna_examples:
        vn.train(question=question, documentation=answer)

def run_query(sql):
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='univ_user',
            password='Univ@1234',
            database='university',
            connect_timeout=5
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute(sql)
        
        # For SELECT queries, return results
        if sql.strip().lower().startswith('select'):
            results = cursor.fetchall()
            return results if results else [{"message": "No results found"}]
        # For other queries, return success message
        else:
            conn.commit()
            return [{"status": "success", "rows_affected": cursor.rowcount}]
            
    except mysql.connector.Error as err:
        error_msg = str(err)
        if 'conn' in locals() and conn.is_connected():
            conn.rollback()  # Rollback in case of error
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals():
            conn.close()
        if 'You have an error in your SQL syntax' in error_msg:
            error_msg = "There is a syntax error in your SQL query. Please check the query and try again."
        elif 'Access denied' in error_msg:
            error_msg = "Access denied. Please check your database credentials."    
            return [{"error": error_msg}]
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def validate_sql(sql):
    forbidden = ['drop', 'delete', 'update', 'insert', 'alter']
    return not any(cmd in sql.lower() for cmd in forbidden)
