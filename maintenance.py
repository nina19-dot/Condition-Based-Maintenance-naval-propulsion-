# maintenance.py


def estado_compresor(kMc):

    degradacion = (
        (1 - kMc) /
        (1 - 0.95)
    ) * 100

    if degradacion >= 80:

        estado = (
            'CRÍTICO - '
            'Evaluar mantenimiento'
        )

    elif degradacion >= 60:

        estado = (
            'REVISIÓN - '
            'Programar inspección'
        )

    else:

        estado = (
            'NORMAL - '
            'Continuar monitoreo'
        )

    return degradacion, estado


def estado_turbina(kMt):

    degradacion = (
        (1 - kMt) /
        (1 - 0.975)
    ) * 100

    if degradacion >= 80:

        estado = (
            'CRÍTICO - '
            'Evaluar mantenimiento'
        )

    elif degradacion >= 60:

        estado = (
            'REVISIÓN - '
            'Programar inspección'
        )

    else:

        estado = (
            'NORMAL - '
            'Continuar monitoreo'
        )

    return degradacion, estado
