from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Category, Product, ProductVariant, ProductImage
from django.utils.html import format_html

# --------------------
# Image Inline (with preview)
# --------------------
class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="border:1px solid #ccc;"/>', obj.image.url)
        return "-"
    image_preview.short_description = 'Preview'

# --------------------
# Variant Inline (with image support)
# --------------------
class ProductVariantInline(admin.StackedInline):
    model = ProductVariant
    extra = 1
    show_change_link = True
    readonly_fields = []
    inlines = [ProductImageInline]

# --------------------
# Category Admin
# --------------------
# @admin.register(Category)
# class CategoryAdmin(admin.ModelAdmin):
#     list_display = ('name', 'slug')
#     prepopulated_fields = {"slug": ("name",)}


# --------------------
# Category Admin (UPDATED)
# --------------------
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'category_image_preview')
    prepopulated_fields = {"slug": ("name",)}
    readonly_fields = ('category_image_preview',)

    def category_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="border:1px solid #ccc; border-radius:4px;" />', obj.image.url)
        return "-"
    category_image_preview.short_description = "Image Preview"

# --------------------
# Product Admin
# --------------------
class ProductVariantInlineInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'base_price', 'created_at')
    list_filter = ('category',)
    search_fields = ('name', 'description')
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductVariantInlineInline]

# --------------------
# Variant Admin (with nested images)
# --------------------
@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ('product', 'color', 'size', 'stock', 'price')
    list_filter = ('color', 'size')
    inlines = [ProductImageInline]

# --------------------
# Image Admin (optional direct access)
# --------------------
@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('variant', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" style="border:1px solid #ccc;"/>', obj.image.url)
        return "-"




from django.contrib import admin
from .models import ProductOffer

@admin.register(ProductOffer)
class ProductOfferAdmin(admin.ModelAdmin):
    list_display = ('product', 'discount_percent', 'start_date', 'end_date', 'is_active')
    list_filter = ('start_date', 'end_date', 'discount_percent')


from django.contrib import admin
from .models import Order, OrderItem, Payment

# Inline display of Order Items
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')
    can_delete = False

# Admin for Order model
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'status', 'total_amount', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'order_id')
    inlines = [OrderItemInline]
    list_editable = ('status',)
    readonly_fields = ('user', 'total_amount', 'created_at', 'updated_at')

# Admin for Payment model
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('order', 'user', 'amount', 'method', 'status', 'created_at')
    list_filter = ('method', 'status', 'created_at')
    search_fields = ('user__username', 'order__order_id')
    list_editable = ('status',)
    readonly_fields = ('order', 'amount', 'user', 'method', 'razorpay_order_id', 'razorpay_payment_id', 'razorpay_signature', 'created_at')



from django.contrib import admin
from .models import ProductReview

@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'is_verified_purchase', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'is_verified_purchase', 'created_at')
    search_fields = ('user__username', 'product__name', 'review_text')
    actions = ['approve_reviews']

    @admin.action(description='Approve selected reviews')
    def approve_reviews(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f"{updated} review(s) approved.")
