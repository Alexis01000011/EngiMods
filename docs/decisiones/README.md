# Registros de decisiones (ADR)

Una decisión técnica o de proveedor por archivo: `NNNN-titulo-corto.md`, numerado en orden. Una decisión aceptada no se edita; si cambia, se escribe una nueva que la reemplace y se marca la anterior como `Reemplazada por NNNN`.

## Plantilla

```markdown
# NNNN. Título

- Estado: Propuesta | Aceptada | Reemplazada por NNNN
- Fecha: AAAA-MM-DD
- Historia: EM-0XX

## Contexto
Qué problema hay que resolver y qué restricciones existen.

## Opciones consideradas
Cada opción con ventajas, desventajas y costo (con fuente y fecha de consulta si aplica).

## Decisión
Qué se eligió y por qué.

## Consecuencias
Qué se vuelve más fácil, qué se vuelve más difícil y qué queda pendiente.
```

## Índice

- [0001. Stack base](0001-stack-base.md)
- [0002. Estilos del frontend (Aceptada)](0002-estilos-frontend.md)
- [0003. Hosting de staging (Aceptada)](0003-hosting-staging.md)
- [0004. Correo transaccional (Propuesta)](0004-correo-transaccional.md)
