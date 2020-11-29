from unittest.mock import patch

from family_foto import Role, add_user


def mock_user(test_case, user_name, role_name) -> None:
    """
    Mocks a user on current_cuser
    :param test_case: test case class, where the user should be mocked
    :param user_name: name of the mocked user
    :param role_name: string of the role name
    """
    test_case.patcher = patch('flask_login.utils._get_user')
    test_case.mock_current_user = test_case.patcher.start()
    user_role = Role.query.filter_by(name=role_name).first()
    user = add_user(user_name, '1234', [user_role])
    test_case.mock_current_user.return_value = user
    test_case.mock_current_user.id = user.id
