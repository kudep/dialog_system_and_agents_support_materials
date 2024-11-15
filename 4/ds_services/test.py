
from services_api import gigachat
from services_api import intent_catcher
print(gigachat.proxy_chain.invoke(gigachat.GigachatRequest(text="test").json()))


print(intent_catcher.proxy_chain.invoke(intent_catcher.IntentCatcherRequest(intent_catcher_request="хочу получить заказ").json()))