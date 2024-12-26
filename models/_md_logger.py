import os
from dotenv import load_dotenv
import logging

load_dotenv()


class Logger:
    """
    Classe de Logger personalizada para gerenciar logs do sistema em diferentes níveis.

    Logs são salvos em arquivos distintos para cada nível e estão preparados para futuras integrações
    com serviços de comunicação em tempo real para erros e exceções.
    """
    _caminho_programa = os.path.join(os.getenv('APPDATA', '.'), os.getenv('APPNAME', 'app'))

    # Definir diretórios e arquivos de log
    _log_dir = os.path.join(_caminho_programa, 'logs')
    info_log_file = os.path.join(_log_dir, 'info.log')
    error_log_file = os.path.join(_log_dir, 'error.log')
    debug_log_file = os.path.join(_log_dir, 'debug.log')

    @staticmethod
    def _setup_logger(name: str, log_file: str, level: int) -> logging.Logger:
        """
        Configura um logger com arquivo de saída específico e nível de log.

        :param name: Nome do logger.
        :param log_file: Caminho do arquivo onde o log será salvo.
        :param level: Nível do log (INFO, ERROR, DEBUG, etc.).
        :return: Instância do logger configurado.
        """
        logger = logging.getLogger(name)
        logger.setLevel(level)

        # Formato do log
        formatter = logging.Formatter('\n[%(asctime)s] [%(levelname)s] %(message)s')

        # Configurar arquivo de log
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)

        # Evitar duplicação de handlers
        if not logger.handlers:
            logger.addHandler(file_handler)

        return logger

    @classmethod
    def info(cls, message: str):
        """
        Registra uma mensagem de informação no arquivo de logs INFO.

        :param message: Mensagem a ser registrada.
        """
        os.makedirs(cls._log_dir, exist_ok=True)
        logger = cls._setup_logger('INFO', cls.info_log_file, logging.INFO)
        logger.info(message)

    @classmethod
    def debug(cls, message: str):
        """
        Registra uma mensagem de depuração no arquivo de logs DEBUG somente se a variável DEBUG estiver ativada.

        :param message: Mensagem a ser registrada.
        """
        if os.getenv('DEBUG', 0) == 1:
            os.makedirs(cls._log_dir, exist_ok=True)
            logger = cls._setup_logger('DEBUG', cls.debug_log_file, logging.DEBUG)
            logger.debug(message)

    @classmethod
    def error(cls, message: str):
        """
        Registra uma mensagem de erro no arquivo de logs ERROR e prepara envio em tempo real.

        :param message: Mensagem a ser registrada.
        """
        os.makedirs(cls._log_dir, exist_ok=True)
        logger = cls._setup_logger('ERROR', cls.error_log_file, logging.ERROR)
        logger.error(message)

        # Preparar notificação em tempo real
        cls._notify_error(message)

    @staticmethod
    def _notify_error(message: str):
        """
        Método para notificar erros em tempo real ao desenvolvedor.

        Neste momento, apenas imprime a intenção, mas pode ser adaptado para integrar com serviços
        como email, Slack, Telegram, ou outros.

        :param message: Mensagem de erro a ser comunicada.
        """
        # Simulação de envio (futuro: integração com APIs de notificações)
        print(f"[ALERTA] Notificação de erro enviada ao desenvolvedor: {message}")