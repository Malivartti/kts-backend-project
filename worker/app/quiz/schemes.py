from app.quiz.models import QuestionType
from app.web.schemes import OkResponseSchema
from marshmallow import (
    Schema,
    ValidationError,
    fields,
    validate,
    validates_schema,
)


class ThemeSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)


class ThemeSingleQuerySchema(Schema):
    theme_id = fields.Int(required=True)


class ThemeUpdateSchema(Schema):
    title = fields.Str(required=False)


class ThemeResponseSchema(OkResponseSchema):
    data = fields.Nested(ThemeSchema)


class ThemeListSchema(Schema):
    themes = fields.List(fields.Nested(ThemeSchema))


class ThemeListResponseSchema(OkResponseSchema):
    data = fields.Nested(ThemeListSchema)


class QuestionSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True)
    theme_id = fields.Int(allow_none=True)
    type = fields.Str(
        required=True, validate=validate.OneOf([t.value for t in QuestionType])
    )
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class QuestionSingleQuerySchema(Schema):
    question_id = fields.Int(required=True)


class OptionalQuestionSchema(Schema):
    user_id = fields.Int(required=False)
    theme_id = fields.Int(required=False)
    type = fields.Str(
        required=False, validate=validate.OneOf([t.value for t in QuestionType])
    )
    title = fields.Str(required=False)


class QuestionUpdateSchema(Schema):
    theme_id = fields.Int(required=False, allow_none=True)
    type = fields.Str(
        required=False, validate=validate.OneOf([t.value for t in QuestionType])
    )
    title = fields.Str(required=False)

    @validates_schema
    def at_least_one_field(self, data, **kwargs):
        if not data:
            raise ValidationError(
                "At least one field must be specified.",
                field_names=["theme_id", "type", "title"],
            )


class QuestionResponseSchema(OkResponseSchema):
    data = fields.Nested(QuestionSchema)


class QuestionListSchema(Schema):
    questions = fields.List(fields.Nested(QuestionSchema))


class QuestionListResponseSchema(OkResponseSchema):
    data = fields.Nested(QuestionListSchema)


class QuestionAddSchema(Schema):
    title = fields.Str(required=True)
    theme_id = fields.Int(required=False)
    type = fields.Str(
        required=True, validate=validate.OneOf([t.value for t in QuestionType])
    )


class AnswerSchema(Schema):
    id = fields.Int(dump_only=True)
    question_id = fields.Int(required=True)
    title = fields.Str(required=True)
    is_correct = fields.Bool(required=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)


class AnswerSingleQuerySchema(Schema):
    answer_id = fields.Int(required=True)


class AnswerUpdateSchema(Schema):
    title = fields.Str(required=False)
    is_correct = fields.Bool(required=False)

    @validates_schema
    def at_least_one_field(self, data, **kwargs):
        if not data:
            raise ValidationError(
                "At least one field must be specified.",
                field_names=["title", "is_correct"],
            )


class AnswerResponseSchema(OkResponseSchema):
    data = fields.Nested(AnswerSchema)


class AnswerListSchema(Schema):
    answers = fields.List(fields.Nested(AnswerSchema))


class AnswerListResponseSchema(OkResponseSchema):
    data = fields.Nested(AnswerListSchema)
