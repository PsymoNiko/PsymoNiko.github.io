from django.db import models
from PIL import Image
from django.utils.text import slugify
from django.core.files import File
from io import BytesIO

class MyBaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    is_deleted = models.BooleanField(default=False, blank=True, null=True)

    class Meta:
        abstract = True


def make_thumbnail(image, size=(140, 140)):
    """Makes thumbnails of given size from given image"""

    im = Image.open(image)

    im.convert('RGB')  # convert mode

    im.thumbnail(size)  # resize image

    thumb_io = BytesIO()  # create a BytesIO object
    im.save(thumb_io, 'png', quality=100)
    file_name = image.name.split('/')[-1]  # Extract the file name from the path
    print(file_name)
    thumb_file_name, file_extension = file_name.rsplit('.', 1)
    print(thumb_file_name)

    thumbnail = File(thumb_io,
                     name=thumb_file_name + "_thumbnail." + file_extension)
    return thumbnail


class UploadFile(MyBaseModel):
    file = models.FileField(null=True, blank=True)
    thumbnail_file = models.ImageField(null=True, blank=True)
    file_tags = models.CharField(max_length=128, null=True, blank=True)
    file_url = models.CharField(max_length=128, null=True, blank=True)
    file_name = models.CharField(max_length=128, null=True, blank=True)
    bucket_name = models.CharField(max_length=128, default="chat-bucket")

    def __str__(self):
        if self.file_tags:
            return str(self.file_tags)
        if self.file_name:
            return str(self.file_name)
        else:
            return "Nothing to"
        # f"Tags: {self.file_tags or 'None'}, Name: {self.file_name or 'None'}"

    def save(self, *args, **kwargs):
        # Check the file extension
        file_extension = self.file.name.split('.')[-1].lower()

        # If the file extension is SVG, do not create a thumbnail
        if file_extension == 'svg':
            self.thumbnail_file = self.file  # Assign the original SVG file as thumbnail
        else:
            # For other file types, create a thumbnail
            thumbnail = make_thumbnail(self.file, size=(300, 300))
            self.thumbnail_file = thumbnail
        super().save(*args, **kwargs)



class Category(MyBaseModel):
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    title = models.CharField(max_length=128)
    slug = models.SlugField(allow_unicode=True)
    level = models.IntegerField(default=0)
    files = models.ManyToManyField(UploadFile, blank=True)
    file_url = models.CharField(max_length=250, blank=True, null=True)

    @property
    def file_clean_url(self):
        if self.file_url:
            return self.file_url
        if self.files.first():
            self.file_url = self.files.first().clean_url
            self.save()
            return self.file_url
        return None

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.parent:
            self.level = self.parent.level + 1
        super(Category, self).save(*args, **kwargs)

    def __str__(self) -> str:
        if not self.parent:
            return f"Mother Category: {self.title}"
        return self.title

    def get_all_parents(self):
        parents = []
        current_parent = self.parent
        while current_parent is not None:
            parents.append(current_parent)
            current_parent = current_parent.parent
        return parents

    def get_all_nested_parents(self):
        nested_parents = []
        current_parent = self.parent
        while current_parent is not None:
            nested_parents.append(current_parent)
            current_parent = current_parent.parent
        for parent in nested_parents:
            nested_parents += parent.get_all_nested_parents()
        return nested_parents

    # def get_products_of_category(self, category):
    #     products = []
    #     selected_category = Category.objects.get(id=category.id)
    #     products += selected_category.product_set.all()
    #     return products
    #
