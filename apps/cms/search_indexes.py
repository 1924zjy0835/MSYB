from haystack import indexes
from .models import Clothes


class ClothesIndex(indexes.SearchIndex, indexes.Indexable):
    # 在类中创建一个属性为text，这个属性必须为text，如果要取其他的名字，就需要在settings中设置以下他的值
    # 做为索引的主要字段
    text = indexes.CharField(document=True, use_template=True)

    # 定义一个get_model()，意为这个模型是为Clothes模型服务的；
    def get_model(self):
        return Clothes

    # 代表以后从Clothes上提取数据的时候，需要返回什么样的值
    def index_queryset(self, using=None):
        return self.get_model().objects.all()
