from fastapi import HTTPException, status


# ── 400 Bad Request ───────────────────────────────────────────────────────────

class BadRequestException(HTTPException):
    def __init__(self, detail: str = "Requisição inválida."):
        super().__init__(status_code=status.HTTP_400_BAD_REQUEST, detail=detail)


# ── 401 Unauthorized ──────────────────────────────────────────────────────────

class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Não autenticado."):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidCredentialsException(UnauthorizedException):
    def __init__(self):
        super().__init__(detail="Email ou senha incorretos.")


class InvalidTokenException(UnauthorizedException):
    def __init__(self):
        super().__init__(detail="Token inválido ou expirado.")


# ── 403 Forbidden ─────────────────────────────────────────────────────────────

class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "Acesso negado."):
        super().__init__(status_code=status.HTTP_403_FORBIDDEN, detail=detail)


# ── 404 Not Found ─────────────────────────────────────────────────────────────

class NotFoundException(HTTPException):
    def __init__(self, resource: str = "Recurso"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} não encontrado.",
        )


# ── 409 Conflict ──────────────────────────────────────────────────────────────

class ConflictException(HTTPException):
    def __init__(self, detail: str = "Conflito com dado existente."):
        super().__init__(status_code=status.HTTP_409_CONFLICT, detail=detail)


class EmailAlreadyExistsException(ConflictException):
    def __init__(self):
        super().__init__(detail="Este e-mail já está cadastrado.")


# ── 422 Unprocessable Entity ─────────────────────────────────────────────────

class UnprocessableException(HTTPException):
    def __init__(self, detail: str = "Dados inválidos."):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
        )


# ── 500 Internal Server Error ─────────────────────────────────────────────────

class InternalServerException(HTTPException):
    def __init__(self, detail: str = "Erro interno do servidor."):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail,
        )