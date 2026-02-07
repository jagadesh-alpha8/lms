# InGage Backend
#
## User Role

### account_role

0 - admin
1 - student
2 - nm api




InGage Project Tables
1. Tables
    1. Users
        1. Username student_id
        2. email
        3. account_role = 0, 1, 2 - nm
        4. Origin - 0 - NM
    2. Courses
        1. course_unique_id
        2. course_name
        3. Descriptions
        4. Image
        5. status
        6. Duration in mins
    3. Course Module
        1. Course_id
        2. module_name
    4. Course Videos
        1. course_id
        2. course_module_id
        3. Title
        4. y_id (video)
        5. Duration in mins
    5. Subscription
        1. user_id
        2. couse_id
        3. origin ( 0 - NM)
        4. reference_id
        5. created
        6. status
        7. course_progress - Float
        8. Certifications | bool
        9. Assignment| bool
    6. Table
        1. user_id
        2. course_id
        3. video_id
    7. TempToken
        1. user_id
        2. status
        3.
