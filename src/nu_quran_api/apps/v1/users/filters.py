import django_filters

from . import models


class UserFilter(django_filters.FilterSet):
    """Filter set for UserViewSet with ordering and search functionality."""

    ordering = django_filters.OrderingFilter(
        fields=(
            ("username", "username"),
            ("email", "email"),
            ("first_name", "first_name"),
            ("last_name", "last_name"),
        ),
        field_labels={
            "username": "Username",
            "email": "Email",
            "first_name": "First Name",
            "last_name": "Last Name",
        },
    )

    email: django_filters.CharFilter = django_filters.CharFilter(
        field_name="email", lookup_expr="icontains"
    )
    username: django_filters.CharFilter = django_filters.CharFilter(
        field_name="username", lookup_expr="icontains"
    )
    first_name: django_filters.CharFilter = django_filters.CharFilter(
        field_name="first_name", lookup_expr="icontains"
    )
    last_name: django_filters.CharFilter = django_filters.CharFilter(
        field_name="last_name", lookup_expr="icontains"
    )
    referrer = django_filters.CharFilter(
        field_name="referrer__username", lookup_expr="exact"
    )
    supervisor = django_filters.CharFilter(
        field_name="supervisor__username", lookup_expr="exact"
    )

    class Meta:
        model = models.User
        fields: list[str] = []


class UserActivitiesFilter(django_filters.FilterSet):
    """Filter set for UserActivitiesViewSet with category and date filtering."""

    ordering = django_filters.OrderingFilter(
        fields=(
            ("date", "date"),
            ("category__id", "category"),
        ),
        field_labels={
            "date": "Activity Date",
            "category__id": "Category",
        },
    )

    category = django_filters.NumberFilter(field_name="category", lookup_expr="exact")
    date = django_filters.DateFromToRangeFilter(field_name="date")

    class Meta:
        model = models.Activity
        fields: list[str] = []


class ActivitiesFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter(field_name="date")
    category = django_filters.NumberFilter(field_name="category", lookup_expr="exact")
    email: django_filters.CharFilter = django_filters.CharFilter(
        field_name="user__email", lookup_expr="icontains"
    )
    username: django_filters.CharFilter = django_filters.CharFilter(
        field_name="user__username", lookup_expr="icontains"
    )
    first_name: django_filters.CharFilter = django_filters.CharFilter(
        field_name="user__first_name", lookup_expr="icontains"
    )
    last_name: django_filters.CharFilter = django_filters.CharFilter(
        field_name="user__last_name", lookup_expr="icontains"
    )
    referrer = django_filters.CharFilter(
        field_name="user__referrer__username", lookup_expr="exact"
    )
    supervisor = django_filters.CharFilter(
        field_name="user__supervisor__username", lookup_expr="exact"
    )

    class Meta:
        model = models.Activity
        fields: list[str] = []


class CategoryFilter(django_filters.FilterSet):
    """Filter set for filtering categories."""

    ordering = django_filters.OrderingFilter(
        fields=(("value", "value"),),
        field_labels={
            "value": "value",
        },
    )

    id: django_filters.NumberFilter = django_filters.NumberFilter(
        field_name="id",
        lookup_expr="exact",
        help_text="Filter categories by ID",
    )
    name: django_filters.CharFilter = django_filters.CharFilter(
        field_name="name", lookup_expr="exact", help_text="Filter categories by name"
    )
    name_ar: django_filters.CharFilter = django_filters.CharFilter(
        field_name="name_ar",
        lookup_expr="icontains",
        help_text="Filter categories by arabic name",
    )
    value: django_filters.NumberFilter = django_filters.NumberFilter(
        field_name="value", lookup_expr="exact", help_text="Filter categories by value"
    )

    class Meta:
        model = models.Category
        fields: list[str] = []
