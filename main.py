from database.database import create_table
from analysis import *
from  config import *
from database import *
def main():
    try:
        conn = config_db()
        
    except Exception as e:
        logger.error(f"Error dalam main: {str(e)}")
        return 1
    return 0

if __name__ == "__main__":
    exit(main())
