MESSAGES_ES: dict[str, str] = {
    # ===== USER MANAGEMENT =====
    # create_user
    "user.email_in_use": "El email ya está en uso",
    "user.username_in_use": "El nombre de usuario ya está en uso",
    "user.created": "Usuario creado exitosamente",
    # confirm_otp
    "user.not_found": "Usuario no encontrado",
    "user.otp.expired_or_invalid": "OTP expirado o inválido",
    "user.otp.invalid": "OTP inválido",
    "user.otp.confirmed": "OTP confirmado exitosamente",
    # change_password
    "user.token.invalid_or_expired": "Token inválido o expirado",
    "user.password_changed": "Contraseña cambiada exitosamente",
    # get_user
    "user.found": "Usuario encontrado",
    # update_user_profile
    "user.username_not_available": "El nombre de usuario no está disponible",
    "user.profile_updated": "Nombre de usuario y nombre actualizados exitosamente",
    # assign_role
    "user.role.invalid": "Rol especificado inválido",
    "user.role.assigned": "Rol asignado exitosamente",
    # update_user_status
    "user.status.invalid": "Estado inválido",
    "user.status.updated": "Estado del usuario actualizado exitosamente",
    # get_connected_users
    "user.connected.none": "No se encontraron usuarios conectados",
    "user.connected.found": "Usuarios conectados encontrados exitosamente",
    # resend_otp
    "user.otp.generic_message": "Si tu cuenta existe, se ha enviado un OTP a tu email registrado",
    # recovery_password
    "user.recovery.url_not_set": "La URL base de recuperación no está configurada en las variables de entorno",
    "user.recovery.email_sent": "Si el email existe en nuestro sistema, recibirás un email de recuperación de contraseña en breve",
    "user.recovery.template_not_found": "Plantilla de email no encontrada. Por favor contacta a soporte",
    "user.recovery.subject": "Instrucciones de recuperación de contraseña",
    # refresh_token
    "user.refresh_token.revoked": "Token de refresh revocado",
    # auth
    "auth.refresh_token.cookie_missing": "Cookie de refresh token faltante",
    "auth.access_token.invalid": "Token de acceso inválido",
    "auth.token.generation_failed": "Error al generar el token",
    # student
    "student.not_found": "Estudiante no encontrado",
    "student.summary.not_found": "Resumen del estudiante no encontrado",
    "student.summary.retrieved": "Resumen del estudiante obtenido exitosamente",
    "student.progress.not_found": "Progreso del estudiante no encontrado",
    "student.progress.retrieved": "Progreso del estudiante obtenido exitosamente",
    "student.retrieved": "Estudiantes obtenidos exitosamente",
    # category
    "category.summary.not_found": "Resumen de categoría no encontrado",
    "category.summary.retrieved": "Resumen de categoría obtenido exitosamente",
    # review
    "reviewer.not_found": "Revisor con ID {reviewer_id} no existe",
    "question.not_found_with_id": "Pregunta con ID {question_id} no existe",
    "review.comments_saved": "Comentarios de revisión guardados exitosamente",
    # question creation
    "question.created": "Pregunta creada exitosamente",
    "question.creation_error": "Error al crear la pregunta",
    # assessment
    "assessment.retrieved": "Evaluación obtenida exitosamente",
    # create_user_from_admin
    "user.admin.default_password_not_set": "La contraseña por defecto no está configurada en las variables de entorno",
    # user_manager_service
    "user.login_url_not_set": "La URL base de login no está configurada en las variables de entorno",
    "user.role.invalid_specified": "Rol especificado inválido",
    "user.account_created_subject": "Tu cuenta ha sido creada exitosamente",
    "user.role.no_users_found": "No se encontraron usuarios para el rol especificado",
    "user.role.retrieved": "Usuarios obtenidos exitosamente",
    # ===== CONTENT MANAGEMENT =====
    # register_content
    "content.duplicate_title": "Ya existe contenido con el mismo título",
    "content.category.invalid": "Categoría proporcionada inválida",
    "content.registered": "Contenido registrado exitosamente",
    # update_resource_content
    "content.updated": "Contenido con ID {content_id} actualizado exitosamente",
    # update_resource_status
    "content.status.cannot_update": "El estado no puede ser actualizado",
    "content.status.updated": "El estado del contenido ha sido actualizado",
    # update_rating
    "content.rating.not_found": "Calificación no encontrada",
    "content.rating.none_found": "No se encontraron calificaciones para el usuario",
    "content.rating.retrieved": "Calificaciones obtenidas exitosamente",
    "content.rating.updated": "Calificación actualizada exitosamente",
    # rate_content
    "content.not_found": "Contenido con ID {content_id} no encontrado",
    "content.rated": "Contenido calificado exitosamente",
    # get_all_contents / get_contents_by_title / get_contents_by_category / get_contents_by_category_topic
    "content.retrieved": "Contenidos obtenidos exitosamente",
    # get_top_best_content
    "content.top.none_found": "No se encontró contenido destacado para el tema proporcionado",
    "content.top.retrieved": "Contenido destacado obtenido exitosamente",
    # get_top_worse_content
    "content.top.worse.none_found": "No se encontró contenido con las calificaciones más bajas para el tema proporcionado",
    "content.top.worse.retrieved": "Contenido con las calificaciones más bajas obtenido exitosamente",
    # get_resource_content / learning paths
    "content.resource.not_found": "Contenido no encontrado",
    "content.resource.retrieved": "Contenido obtenido exitosamente",
    "content.learning_path.retrieval_failed": "No se pudieron obtener las rutas de aprendizaje",
    "content.learning_path.retrieved": "Rutas de aprendizaje obtenidas exitosamente",
    # Reports
    "report.users.retrieved": "Usuarios obtenidos exitosamente",
    "report.students.retrieved": "Estudiantes obtenidos exitosamente",
    "report.category_summary.not_found": "Resumen de categoría no encontrado",
    # ===== ASSESSMENTS =====
    # Question retrieval
    "question.retrieved": "Pregunta obtenida exitosamente",
    "question.retrieval_failed": "No se pudo obtener la pregunta: {error}",
    "question.list.none_found": "No se encontraron preguntas",
    "question.list.retrieved": "Preguntas obtenidas exitosamente",
    "question.list.retrieval_failed": "Ocurrió un error al obtener las preguntas: {error}",
    "question.versions.none_found": "No se encontraron versiones de la pregunta",
    "question.versions.retrieved": "Versiones de la pregunta obtenidas exitosamente",
    "question.categories.retrieval_failed": "No se pudieron obtener las categorías de preguntas",
    "question.categories.retrieved": "Categorías de preguntas obtenidas exitosamente",
    "question.topic.none_found": "No se encontraron temas",
    "question.topic.published.retrieved": "Temas publicados obtenidos exitosamente",
    "question.pending_approval.retrieval_failed": "No se pudieron obtener las preguntas pendientes de aprobación",
    "question.pending_approval.none_found": "No se encontraron preguntas pendientes de aprobación",
    "question.pending_approval.retrieved": "Preguntas pendientes de aprobación obtenidas exitosamente",
    "question.pending_approval.invalid_request": "Solicitud inválida: {error}",
    # Assessment retrieval
    "assessment.retrieval_failed": "No se pudo obtener la evaluación: {error}",
    "assessment.summary.none_found": "No se encontraron evaluaciones para el estudiante",
    "assessment.summary.retrieved": "Resumen de evaluaciones obtenido exitosamente",
    "assessment.result.not_found": "Resultado de evaluación no encontrado",
    "assessment.result.retrieved": "Resultado de evaluación obtenido exitosamente",
    # Model selection
    "model.selected.none_found": "No se encontraron modelos seleccionados",
    "model.selected.retrieved": "Modelos seleccionados obtenidos exitosamente",
    "model.selected.retrieval_failed": "No se pudieron obtener los modelos seleccionados: {error}",
    "model.available.none_found": "No se encontraron modelos disponibles",
    "model.available.retrieved": "Modelos disponibles obtenidos exitosamente",
    "model.available.retrieval_failed": "No se pudieron obtener los modelos disponibles: {error}",
    # register_question
    "question.register.invalid_difficulty": "Error al registrar pregunta: Dificultad inválida '{difficulty}'",
    "question.register.unknown_error": "Error al registrar pregunta: Error desconocido",
    "question.register.failed": "Error al registrar pregunta: {message}",
    # update_question
    "question.update.invalid_difficulty": "Error al actualizar pregunta: Dificultad inválida '{difficulty}'",
    "question.not_found": "Pregunta no encontrada",
    "question.updated": "Pregunta actualizada exitosamente",
    "question.update.failed": "Error al actualizar pregunta: {message}",
    # update_question_status
    "question.status.not_found": "Pregunta con ID {question_id} no encontrada",
    "question.status.updated": "Estado de pregunta actualizado exitosamente",
    # save_assessments_answers
    "assessment.user_not_found": "Usuario no encontrado",
    "assessment.quiz.not_found": "Quiz de evaluación no encontrado para el ID de evaluación proporcionado",
    "assessment.answers.already_exist": "Ya existen respuestas para el ID de evaluación proporcionado",
    "assessment.not_belong_to_user": "El quiz de evaluación no pertenece al usuario",
    "assessment.answers.invalid_question_ids": "IDs de preguntas respondidas inválidos. Deben coincidir con las preguntas del quiz de evaluación",
    "assessment.answers.saved": "Respuestas de evaluación guardadas exitosamente",
    "assessment.error": "Ocurrió un error: {message}",
    # save_review_question
    "question.review.invalid_status": "Estado inválido '{status}'. Los estados válidos son: {valid_statuses}",
    # update_model
    "model.process.invalid": "Proceso especificado inválido",
    "model.id.not_found": "ID de modelo no encontrado en los modelos disponibles",
    "model.updated": "Modelo actualizado exitosamente",
    # evaluate
    "assessment.evaluation.no_qualifications": "No se generaron calificaciones para la evaluación",
    "assessment.evaluation.completed": "Evaluación completada exitosamente",
    # get_quantity_of_assessments
    "assessment.quantity.retrieved": "Cantidad de evaluaciones obtenida exitosamente",
    # ===== VALIDATION MESSAGES =====
    # user validation
    "validation.email.required": "Email es requerido",
    "validation.email.min_length": "Email debe tener al menos 5 caracteres",
    "validation.email.max_length": "Email no debe exceder 255 caracteres",
    "validation.email.format": "Formato de email inválido",
    "validation.email.invalid_format": "Formato de email inválido",
    "validation.username.required": "Nombre de usuario es requerido",
    "validation.username.min_length": "Nombre de usuario debe tener al menos 3 caracteres",
    "validation.username.max_length": "Nombre de usuario no debe exceder 20 caracteres",
    "validation.username.invalid_format": "Nombre de usuario debe ser alfanumérico y puede incluir guiones bajos",
    "validation.name.required": "Nombre es requerido",
    "validation.name.min_length": "Nombre debe tener al menos 3 caracteres",
    "validation.name.max_length": "Nombre no debe exceder 100 caracteres",
    "validation.password.required": "Contraseña es requerida",
    "validation.password.min_length": "Contraseña debe tener al menos 6 caracteres",
    "validation.password.max_length": "Contraseña no debe exceder 20 caracteres",
    "validation.password.digit": "Contraseña debe contener al menos un dígito",
    "validation.password.letter": "Contraseña debe contener al menos una letra",
    "validation.password.special": "Contraseña debe contener al menos un carácter especial",
    "validation.password.must_contain_digit": "Contraseña debe contener al menos un dígito",
    "validation.password.must_contain_letter": "Contraseña debe contener al menos una letra",
    "validation.password.must_contain_special": "Contraseña debe contener al menos un carácter especial",
    # content validation
    "validation.title.required": "Título no debe estar vacío",
    "validation.title.min_length": "Título debe tener al menos 5 caracteres",
    "validation.title.min_length_3": "Título debe tener al menos 3 caracteres",
    "validation.title.min_length_5": "Título debe tener al menos 5 caracteres",
    "validation.title.max_length": "Título no debe exceder 150 caracteres",
    "validation.title.max_length_100": "Título no debe exceder 100 caracteres",
    "validation.title.max_length_150": "Título no debe exceder 150 caracteres",
    "validation.description.required": "Descripción no debe estar vacía",
    "validation.description.min_length": "Descripción debe tener al menos 10 caracteres",
    "validation.description.max_length": "Descripción no debe exceder 300 caracteres",
    "validation.url.required": "URL no debe estar vacía",
    "validation.url.invalid_format": "Formato de URL inválido, debe comenzar con https://",
    # assessment validation
    "validation.score.range": "Puntuación debe estar entre 0 y 3",
    "validation.criteria.required": "Criterio no puede estar vacío",
    "validation.criteria.max_length": "Criterio no puede exceder 300 caracteres",
    "validation.criteria.min_length": "Criterio debe tener al menos 10 caracteres",
    "validation.text.required": "Texto no puede estar vacío",
    "validation.text.max_length": "Texto no puede exceder 500 caracteres",
    "validation.text.min_length": "Texto debe tener al menos 20 caracteres",
    "validation.concept.required": "Concepto no puede estar vacío",
    "validation.concept.max_length": "Concepto no puede exceder 150 caracteres",
    "validation.concept.min_length": "Concepto debe tener al menos 10 caracteres",
    "validation.definition.required": "Definición no puede estar vacía",
    "validation.definition.max_length": "Definición no puede exceder 500 caracteres",
    "validation.definition.min_length": "Definición debe tener al menos 20 caracteres",
    "validation.simple_explanation.required": "Explicación simple no puede estar vacía",
    "validation.simple_explanation.max_length": "Explicación simple no puede exceder 300 caracteres",
    "validation.simple_explanation.min_length": "Explicación simple debe tener al menos 20 caracteres",
    "validation.correct_sample.required": "Ejemplo correcto no puede estar vacío",
    "validation.correct_sample.max_length": "Ejemplo correcto no puede exceder 300 caracteres",
    "validation.correct_sample.min_length": "Ejemplo correcto debe tener al menos 20 caracteres",
    "validation.wrong_sample.required": "Ejemplo incorrecto no puede estar vacío",
    "validation.wrong_sample.max_length": "Ejemplo incorrecto no puede exceder 300 caracteres",
    "validation.wrong_sample.min_length": "Ejemplo incorrecto debe tener al menos 20 caracteres",
    "validation.common_misconception.required": "Conceptos erróneos comunes no puede estar vacío",
    "validation.common_misconception.min_items": "Conceptos erróneos comunes debe tener al menos 2 elementos",
    "validation.common_misconception.item_max_length": "Cada concepto erróneo común no puede exceder 300 caracteres",
    "validation.common_misconception.item_min_length": "Cada concepto erróneo común debe tener al menos 20 caracteres",
    "validation.semantic_keywords.required": "Palabras clave semánticas no puede estar vacío",
    "validation.semantic_keywords.min_items": "Palabras clave semánticas debe tener al menos 1 elemento",
    "validation.semantic_keywords.item_max_length": "Cada palabra clave semántica no puede exceder 100 caracteres",
    "validation.semantic_keywords.item_min_length": "Cada palabra clave semántica debe tener al menos 2 caracteres",
    "validation.difficulty.required": "Dificultad no puede estar vacía",
    "validation.difficulty.max_length": "Dificultad no puede exceder 30 caracteres",
    "validation.difficulty.min_length": "Dificultad debe tener al menos 4 caracteres",
    "validation.topic.required": "Tema no puede estar vacío",
    "validation.topic.max_length": "Tema no puede exceder 100 caracteres",
    "validation.topic.min_length": "Tema debe tener al menos 2 caracteres",
    "validation.previous_version_id.max_length": "ID de versión anterior no puede exceder 100 caracteres",
    "validation.root_version_id.max_length": "ID de versión raíz no puede exceder 100 caracteres",
    # review question validation
    "validation.question_id.required": "question_id no debe estar vacío",
    "validation.question_id.min_length": "question_id debe tener al menos 5 caracteres",
    "validation.question_id.max_length": "question_id no debe exceder 100 caracteres",
    "validation.reviewer_id.required": "reviewer_id no debe estar vacío",
    "validation.reviewer_id.min_length": "reviewer_id debe tener al menos 5 caracteres",
    "validation.reviewer_id.max_length": "reviewer_id no debe exceder 100 caracteres",
    "validation.review_comments.required": "review_comments no debe estar vacío",
    "validation.review_comments.min_length": "review_comments debe tener al menos 10 caracteres",
    "validation.review_comments.max_length": "review_comments no debe exceder 1000 caracteres",
    "validation.status.required": "status no debe estar vacío",
    # ===== ADDITIONAL VALIDATION MESSAGES =====
    # User ID validation
    "validation.user_id.required": "ID de usuario no debe estar vacío",
    "validation.user_id.min_length_1": "ID de usuario debe tener al menos 1 carácter",
    "validation.user_id.min_length_5": "ID de usuario debe tener al menos 5 caracteres",
    "validation.user_id.min_length_10": "ID de usuario debe tener al menos 10 caracteres",
    "validation.user_id.max_length": "ID de usuario no debe exceder 100 caracteres",
    # Username validation (additional)
    "validation.username.no_special": "Nombre de usuario no debe contener caracteres especiales",
    "validation.username.no_spaces": "Nombre de usuario no debe contener espacios",
    # Content ID validation
    "validation.content_id.required": "ID de contenido no debe estar vacío",
    "validation.content_id.min_length": "ID de contenido debe tener al menos 10 caracteres",
    "validation.content_id.max_length": "ID de contenido no debe exceder 100 caracteres",
    # Category validation
    "validation.category.required": "Categoría no debe estar vacía",
    "validation.category.min_length": "Categoría debe tener al menos 3 caracteres",
    "validation.category.max_length_80": "Categoría no debe exceder 80 caracteres",
    "validation.category.max_length_100": "Categoría no debe exceder 100 caracteres",
    # Topic validation (additional)
    "validation.topic.min_length": "Tema debe tener al menos 3 caracteres",
    # Title validation (additional)
    "validation.title.min_length_3": "Título debe tener al menos 3 caracteres",
    "validation.title.max_length_100": "Título no debe exceder 100 caracteres",
    # URL validation
    "validation.url.required": "URL no debe estar vacía",
    "validation.url.format": "Formato de URL inválido, debe comenzar con https://",
    # Page/Pagination validation
    "validation.page.non_negative": "Número de página debe ser un entero no negativo",
    "validation.page_size.min": "Tamaño de página debe ser al menos 1",
    "validation.page_size.max": "Tamaño de página no debe exceder 100",
    "validation.page_size.range": "Tamaño de página debe estar entre 1 y 100",
    # Rating validation
    "validation.rating.range": "Calificación debe estar entre 0 y 5",
    # Role validation
    "validation.role.required": "Rol no debe estar vacío",
    "validation.role.min_length": "Rol debe tener al menos 3 caracteres",
    "validation.role.max_length": "Rol no debe exceder 20 caracteres",
    # Status validation (additional)
    "validation.status.min_length": "Estado debe tener al menos 3 caracteres",
    "validation.status.max_length": "Estado no debe exceder 20 caracteres",
    "validation.status.boolean": "Estado debe ser un valor booleano",
    # Student ID validation
    "validation.student_id.required": "student_id no debe estar vacío",
    "validation.student_id.min_length": "student_id debe tener al menos 5 caracteres",
    "validation.student_id.max_length": "student_id no debe exceder 100 caracteres",
    # Limit validation
    "validation.limit.range": "Límite debe estar entre 1 y 50",
    # Assessment validation
    "validation.assessment.required": "Datos de evaluación son requeridos para evaluación",
    # ===== GLOBAL =====
    "error.unexpected": "Ocurrió un error inesperado",
    "learning_path.created": "Ruta de aprendizaje creada exitosamente",
    "learning_path.failed": "Error al crear la ruta de aprendizaje",
    "learning_path.not_found": "La ruta de aprendizaje no fue encontrada",
    "learning_path.exists": "La ruta de aprendizaje ya existe y no está completada. Debe completarla antes de crear una nueva",
    "learning_path.completed": "La ruta de aprendizaje ha sido completada exitosamente",
    "learning_path.retrieved": "La ruta de aprendizaje ha sido recuperada con éxito",
    "validation.path_id.required": "ID de ruta no debe estar vacío",
    "validation.path_id.min_length": "ID de ruta debe tener al menos 5 caracteres",
    "validation.path_id.max_length": "ID de ruta no debe exceder 100 caracteres",
    "content.learning_path.retrieval_failed": "Error al recuperar la ruta de aprendizaje",
    "content.learning_path.retrieved": "Ruta de aprendizaje recuperada exitosamente",
}


def t(key: str, **kwargs) -> str:
    """Translate a message key to Spanish with optional interpolation.

    Args:
        key: The message key to look up in the catalog.
        **kwargs: Optional interpolation values for dynamic messages.

    Returns:
        The translated message, or a placeholder if the key is missing.
    """
    msg = MESSAGES_ES.get(key)
    if msg is None:
        return f"[missing: {key}]"
    if kwargs:
        try:
            msg = msg.format(**kwargs)
        except KeyError:
            pass
    return msg
