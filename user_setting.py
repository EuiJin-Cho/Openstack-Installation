from keystoneauth1 import identity
from keystoneauth1 import session
from keystoneclient.v3 import client as kClient

auth = identity.V3Password(auth_url='http://192.168.49.10/identity',
                           username='admin',
                           user_domain_name='Default',
                           password='ckddmlrhks401!',
                           project_name='admin',
                           project_domain_name='Default')

sess = session.Session(auth=auth)
keystone = kClient.Client(session=sess)

role_list = keystone.roles.list()
num_of_student = 15
for i in range(num_of_student):
    role_id = ""
    admin_role_id = ""
    admin_id = ""
    stu_num = i + 16
    project_name = "student" + str(stu_num)
    vm_project = keystone.projects.create(name=project_name, domain="default")
    for role in role_list:
        print(role.name, end="  ")
    print("\n")
    role_name = "member"
    admin_role_name = "admin"
    for role in role_list:
        if role.name == role_name:
            role_id = role.id

    for role in role_list:
        if role.name == admin_role_name:
            admin_role_id = role.id

    user_list = keystone.users.list()
    for user in user_list:
        if user.name == admin_role_name:
            admin_id = user.id

    project_user_name = "student" + str(stu_num)
    project_user_passwd = "cloudstudent" + str(stu_num) + "!@#$"
    project_user = keystone.users.create(name=project_user_name,
                                         domain="default",
                                         password=project_user_passwd)

    ROLE_ID = role_id
    USER_ID = project_user.id
    PROJECT_ID = vm_project.id

    keystone.roles.grant(role=ROLE_ID, user=USER_ID, project=PROJECT_ID)
    keystone.roles.grant(role=admin_role_id, user=admin_id, project=PROJECT_ID)
