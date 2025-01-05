# producer/__init__.py

# Import fungsi-fungsi yang ingin kita expose dari producer.py
from .producer import create_producer, produce_message

# Optional: Bisa menambahkan __all__ untuk mendefinisikan apa yang bisa di-import
__all__ = ['create_producer', 'produce_message']


__version__ = '0.1.0'