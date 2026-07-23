# 環境變數/配置管理

from pydantic_settings import BaseSettings


#定義配置類別，繼承自 BaseSettings，用於管理應用程式的環境變數和配置。
class Settings(BaseSettings):
    openai_api_key: str = ""
    openai_model: str = "gpt-4o-mini"
    openai_base_url: str = "https://api.openai.com/v1"

    debug: bool = True

#告訴 Pydantic 在實例化時，要去專案根目錄尋找名為 .env 的檔案。
#如果 .env 檔案存在，它會讀取裡面的內容（例如 OPENAI_API_KEY=sk-xxxx...）並覆蓋掉上面定義的預設值。
    class Config:
        env_file = ".env"

#在專案的其他檔案中，你只需要匯入這個 settings 變數，就可以輕鬆取得配置
settings = Settings()
