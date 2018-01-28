from django.db import models
from django import forms
from django.utils.safestring import mark_safe

from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore import blocks
from wagtail.wagtailcore.blocks import CharBlock, ChoiceBlock, RichTextBlock, TextBlock

from wagtail.wagtailcore.fields import StreamField

from wagtail.wagtailadmin.edit_handlers import FieldPanel, StreamFieldPanel

from wagtail.wagtailimages.blocks import ImageChooserBlock
#from wagtail.wagtailimages.fields import ImageField
from wagtail.wagtailimages.edit_handlers import ImageChooserPanel

from wagtail.wagtailembeds.blocks import EmbedBlock

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.wagtailsnippets.models import register_snippet
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager

from taggit.models import TaggedItemBase, Tag as TaggitTag

from pygments import highlight
from pygments.formatters import get_formatter_by_name
from pygments.lexers import get_lexer_by_name

from wagtail.contrib.wagtailroutablepage.models import RoutablePageMixin, route

from wagtail.wagtailsearch import index

# Create your models here.
class HomePage(RoutablePageMixin, Page):

    def get_posts(self):
        return PostPage.objects.child_of(self).live().order_by('-first_published_at')

    def get_context(self, request):
        context = super(HomePage, self).get_context(request)
        #posts = PostPage.objects.child_of(self).live().order_by('-first_published_at')

        # Pagination
        page = request.GET.get('page')
        paginator = Paginator(self.posts, 2)  # Show 6 pages per page
        try:
            pages = paginator.page(page)
        except PageNotAnInteger:
            pages = paginator.page(1)
        except EmptyPage:
            pages = paginator.page(paginator.num_pages)

        context['pages'] = pages
        context['home_page'] = self
        return context


    @route(r'^tag/(?P<tag>[-\w]+)/$')
    def post_by_tag(self, request, tag, *args, **kwargs):
        self.posts = self.get_posts().filter(tags__slug=tag)
        return Page.serve(self, request, *args, **kwargs)


    @route(r'^$')
    def post_list(self, request, *args, **kwargs):
        self.posts = self.get_posts()
        return Page.serve(self, request, *args, **kwargs)
        
    @route(r'^search/$')
    def post_search(self,request,*args,**kwargs):
        search_query = request.GET.get('q', None)
        print(search_query)
        self.posts = self.get_posts()

        if search_query:
            self.posts = self.posts.filter(body__icontains=search_query)
            self.search_term = search_query
            self.search_type = 'search'

        return Page.serve(self, request, *args, **kwargs)


class CodeBlock(blocks.StructBlock):

    LANGUAGE_CHOICES = [
        ('arduino', 'Arduino'),
        ('bash', 'Shell'),
        ('c', 'C'),
        ('css', 'CSS'),
        ('django', 'Django'),
        ('docker', 'Docker'),
        ('javascript', 'JavaScript'),
        ('json', 'JSON'),
        ('md', 'Markdown'),
        ('nginx', 'Nginx'),
        ('plpgsql', 'Pl/pgSQL'),
        ('postgresql', 'PostgreSQL'),
        ('python', 'Python'),
        ('sql', 'SQL'),
        ('sqlite3', 'SQLite3'),
        ('yaml', 'YAML'),
    ]

    STYLE_CHOICES = [
        ('syntax', 'default'),
    ]

    language = ChoiceBlock(choices=LANGUAGE_CHOICES)
    style = ChoiceBlock(choices=STYLE_CHOICES, default='syntax')
    code = TextBlock()

    def render(self, value, context):
        src = value['code'].strip('\n')
        lang = value['language']
        lexer = get_lexer_by_name(lang)
        css_classes = ['code', value['style']]

        formatter = get_formatter_by_name(
            'html',
            linenos = None,
            #cssclass = ' '.join(css_classes),
            cssclass = 'syntax',
            #style = 'default',
            noclasses = False,
        )

        return mark_safe(highlight(src, lexer, formatter))

    class Meta:
        icon = 'code'

class LeftAlignedCodeBlock(blocks.StructBlock):

    left_column = blocks.StreamBlock([
        ('code', CodeBlock()),
    ])

    right_column = blocks.StreamBlock([
        ('paragraph', blocks.RichTextBlock()),
    ])

    class Meta:
        template = 'blog/left_aligned_code_block.html'
        icon = 'code'


class RightAlignedCodeBlock(blocks.StructBlock):

    left_column = blocks.StreamBlock([
        ('paragraph', blocks.RichTextBlock()),
    ])

    right_column = blocks.StreamBlock([
        ('code', CodeBlock()),
    ])

    class Meta:
        template = 'blog/right_aligned_code_block.html'
        icon = 'code'


class TwoColumnCodeBlock(blocks.StructBlock):

    left_column = blocks.StreamBlock([
        ('left_code', CodeBlock()),
    ])

    right_column = blocks.StreamBlock([
        ('right_code', CodeBlock()),
    ])

    class Meta:
        template = 'blog/two_column_code_block.html'
        icon = 'code'


class LeftAlignedImage(blocks.StructBlock):

    left_column = blocks.StreamBlock([
        ('image', ImageChooserBlock()),
    ])

    right_column = blocks.StreamBlock([
        ('paragraph', blocks.RichTextBlock())
    ])

    class Meta:
        template = 'blog/left_aligned_image.html'
        icon = 'image'


class RightAlignedImage(blocks.StructBlock):

    left_column = blocks.StreamBlock([
        ('paragraph', blocks.RichTextBlock())
    ])

    right_column = blocks.StreamBlock([
        ('image', ImageChooserBlock()),
    ])

    class Meta:
        template = 'blog/right_aligned_image.html'
        icon = 'image'


class PostPage(Page):

    date = models.DateField(auto_now=True)
    header_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    body = StreamField([
        ('post_heading', CharBlock(max_length=40)),
        ('section_heading', CharBlock(max_length=40)),
        ('inline_image', ImageChooserBlock()),
        ('panorama_image', ImageChooserBlock()),
        ('paragraph', RichTextBlock()),
        ('code', CodeBlock()),
        ('video', EmbedBlock()),
        ('left_aligned_image', LeftAlignedImage()),
        ('right_aligned_image', RightAlignedImage()),
        ('two_column_code_block', TwoColumnCodeBlock()),
        ('left_aligned_code_block', LeftAlignedCodeBlock()),
        ('right_aligned_code_block', RightAlignedCodeBlock()),
    ])

    categories = ParentalManyToManyField('blog.PostPageCategory', blank=True)
    tags = ClusterTaggableManager(through='blog.PostPageTag', blank=True)

    content_panels = Page.content_panels + [
        ImageChooserPanel('header_image'),
        StreamFieldPanel('body'),
        FieldPanel('categories', widget=forms.CheckboxSelectMultiple),
        FieldPanel('tags'),
    ]

    search_fields = Page.search_fields + [
        index.SearchField('body'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super(PostPage, self).get_context(request, *args, **kwargs)
        context['home_page'] = self.get_parent().specific
        context['post'] = self
        return context


@register_snippet
class PostPageCategory(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True,max_length=50)

    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"


class PostPageTag(TaggedItemBase):
    content_object = ParentalKey('PostPage', related_name='post_tags')


@register_snippet
class Tag(TaggitTag):
    class Meta:
        proxy = True


