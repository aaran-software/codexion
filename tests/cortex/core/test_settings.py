# import os
# from cortex.core.settings import Settings
#
# def test_settings_env_loading(monkeypatch):
#     # Override .env values using monkeypatch (simulates loading from .env)
#     monkeypatch.setenv("TESTING", "true")
#     monkeypatch.setenv("DB_ENGINE", "test_mysql")
#     monkeypatch.setenv("DB_HOST", "test_localhost")
#     monkeypatch.setenv("DB_PORT", "3307")
#     monkeypatch.setenv("DB_USER", "test_root")
#     monkeypatch.setenv("DB_PASS", "test_Computer.1")
#     monkeypatch.setenv("DB_NAME", "test_codexion_db")
#     monkeypatch.setenv("JWT_SECRET_KEY", "testsecret")
#
#     settings = Settings()
#
#     assert settings.TESTING is True
#     assert settings.DB_ENGINE == "test_mysql"
#     assert settings.DB_HOST == "test_localhost"
#     assert settings.DB_PORT == 3307
#     assert settings.DB_USER == "test_root"
#     assert settings.DB_PASS == "test_Computer.1"
#     assert settings.DB_NAME == "test_codexion_db"
#     assert settings.JWT_SECRET_KEY == "testsecret"
#
#
# # def test_settings_of_env():
# #
# #     settings = Settings()
# #
# #     assert settings.TESTING is True
# #     assert settings.DB_ENGINE == "mysql"
# #     assert settings.DB_HOST == "localhost"
# #     assert settings.DB_PORT == 3306
# #     assert settings.DB_USER == "root"
# #     assert settings.DB_PASS == "Computer.1"
# #     # assert settings.DB_NAME == "codexion_db"
# #     assert settings.JWT_SECRET_KEY == "your_super_secret_key_here"
