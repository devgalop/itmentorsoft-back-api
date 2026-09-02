from itmentorsoft_persistence.dto import (
    ResourceContent,
    ResourceContentBuilder,
    ContentCategory,
    PaginatedResourceContentResult,
)


def test_add_content_id_updates_content_id_on_resource_content():
    content = ResourceContent()
    content.add_content_id("custom-id-123")
    assert content.content_id == "custom-id-123"


def test_builder_set_content_id_returns_builder_and_updates_id():
    builder = ResourceContentBuilder()
    result = builder.set_content_id("abc-123")
    assert result is builder
    assert builder.build().content_id == "abc-123"


def test_builder_set_content_id_chained_with_full_build():
    content = (
        ResourceContentBuilder()
        .set_content_id("my-id")
        .set_title("Title")
        .set_summary("Summary")
        .set_url("https://example.com")
        .set_category(ContentCategory.NOVICE)
        .add_related_topics(["Python"])
        .build()
    )
    assert content.content_id == "my-id"
    assert content.title == "Title"
    assert content.summary == "Summary"
    assert content.url == "https://example.com"
    assert content.category == ContentCategory.NOVICE
    assert content.related_topics == ["Python"]


def test_paginated_resource_content_result_stores_items_and_total():
    result = PaginatedResourceContentResult(items=[], total=0)
    assert result.items == []
    assert result.total == 0
