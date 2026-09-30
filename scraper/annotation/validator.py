class AnnotationValidator:

    VALID_KBLI = set("ABCDEFGHIJKLMNOPQRSTU")

    VALID_DIRECTIONS = {
        "meningkat",
        "menurun",
        "netral",
    }

    @classmethod
    def validate(
        cls,
        phenomenon_annotation,
        kbli_annotation,
        direction_annotation,
    ):
        errors = []

        # Validasi fenomena
        if phenomenon_annotation is None:
            errors.append(
                "Anotasi fenomena wajib diisi."
            )

        # Jika bukan fenomena ekonomi
        if phenomenon_annotation is False:

            if kbli_annotation is not None:
                errors.append(
                    "KBLI harus kosong jika fenomena = False."
                )

            if direction_annotation is not None:
                errors.append(
                    "Arah harus kosong jika fenomena = False."
                )

        # Jika merupakan fenomena ekonomi
        if phenomenon_annotation is True:

            if kbli_annotation not in cls.VALID_KBLI:
                errors.append(
                    "KBLI harus berupa kategori A sampai U."
                )

            if direction_annotation not in cls.VALID_DIRECTIONS:
                errors.append(
                    "Arah harus meningkat, menurun, atau netral."
                )

        return {
            "valid": len(errors) == 0,
            "errors": errors,
        }