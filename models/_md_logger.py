import datetime
from dotenv import load_dotenv
import os

load_dotenv()

# class SimpleLogger:
#     def __init__(self):
#         """
#         Inicializa o logger.
#
#         :param log_file: Caminho para o arquivo onde os logs serão armazenados.
#         """
#         self.log_file = os.path.join(os.getenv('APPDATA'), os.getenv('APPNAME'), 'Log')
#
#     def _write_log(self, level, message):
#         """
#         Escreve a mensagem de log no arquivo e exibe no console.
#
#         :param level: Nível do log (INFO ou ERROR).
#         :param message: Mensagem a ser registrada.
#         """
#         timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
#         log_message = f"[{timestamp}] [{level}] {message}"
#
#         # Salva no arquivo de log
#         with open(self.log_file, 'a') as file:
#             file.write(log_message + '\n')
#
#         # Exibe no console
#         print(log_message)
#
#     def info(self, message):
#         """
#         Registra uma mensagem de informação.
#
#         :param message: Mensagem a ser registrada.
#         """
#         self._write_log('INFO', message)
#
#     def error(self, message):
#         """
#         Registra uma mensagem de erro.
#
#         :param message: Mensagem a ser registrada.
#         """
#         self._write_log('ERROR', message)
class Logger:
    _caminho_programa = os.path.join(os.getenv('APPDATA'), os.getenv('APPNAME'))

    info_log_file = os.path.join(_caminho_programa, 'logs', 'info.log')
    error_log_file = os.path.join(_caminho_programa, 'logs', 'error.log')
    dev_log_file = os.path.join(_caminho_programa, 'logs', 'dev.log')

    @staticmethod
    def _write_log(level, message, log_file):
        """
        Escreve a mensagem de log no arquivo específico e exibe no console.

        :param level: Nível do log (INFO ou ERROR).
        :param message: Mensagem a ser registrada.
        :param log_file: Arquivo onde o log será salvo.
        """
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_message = f"[{timestamp}] [{level}] {message}"

        # Salva no arquivo de log
        with open(log_file, 'a') as file:
            file.write(log_message + '\n')

        # Exibe no console
        print(log_message)

    @classmethod
    def info(cls, message):
        """
        Registra uma mensagem de informação no arquivo de informações.

        :param message: Mensagem a ser registrada.
        """
        cls._write_log('INFO', message, cls.info_log_file)

    @classmethod
    def error(cls, message):
        """
        Registra uma mensagem de erro no arquivo de erros.

        :param message: Mensagem a ser registrada.
        """
        cls._write_log('ERROR', message, cls.error_log_file)

    @classmethod
    def dev(cls, message):
        """
        Registra uma mensagem de erro no arquivo de dev.

        :param message: Mensagem a ser registrada.
        """
        cls._write_log('DEV', message, cls.error_log_file)