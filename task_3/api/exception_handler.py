from drf_standardized_errors import formatter, types


class Formatter(formatter.ExceptionFormatter):
    def format_error_response(self, error_response: types.ErrorResponse) -> dict:
        error = error_response.errors[0]
        return {
            'type': error_response.type,
            'code': error.code,
            'message': error.detail,
            'field_name': error.attr,
        }
