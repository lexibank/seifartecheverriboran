import attr
import pathlib
from clldutils.misc import slug
from pylexibank import Dataset as BaseDataset
from pylexibank import progressbar as pb
from pylexibank import Lexeme
from pylexibank import FormSpec
from lingpy import Wordlist


@attr.s
class CustomLexeme(Lexeme):
    ProtoForm = attr.ib(default=None)
    ProtoSet = attr.ib(default=None)
    APBM = attr.ib(default=None)
    BasicVocabulary = attr.ib(default=None)
    Morphemes = attr.ib(default=None)


class Dataset(BaseDataset):
    dir = pathlib.Path(__file__).parent
    id = "seifartecheverriboran"
    lexeme_class = CustomLexeme
    form_spec = FormSpec(
            separators=", "
            )

    def cmd_makecldf(self, args):
        # add bib
        args.writer.add_sources()
        args.log.info("added sources")

        # add concept
        concepts = {}
        for concept in self.concepts:
            idx = concept["ID"] + "_" + slug(concept["ENGLISH"])
            args.writer.add_concept(
                ID=idx,
                Name=concept["ENGLISH"],
                Concepticon_ID=concept["CONCEPTICON_ID"],
                Concepticon_Gloss=concept["CONCEPTICON_GLOSS"],
            )
            concepts[concept["ENGLISH"]] = idx

        args.log.info("added concepts")

        # add language
        for language in self.languages:
            args.writer.add_language(
                    ID=language["ID"],
                    Name=language["Name"],
                    Glottocode=language["Glottocode"]
                    )
        args.log.info("added languages")

        # add data
        wl = Wordlist(str(self.raw_dir.joinpath("parsed_bora.tsv")))
        for (
            idx,
            doculect,
            form,
            concept,
            cogid,
            morphemes,
            note,
            protoset,
            protoform,
            apbm,
            basicvocabulary
        ) in pb(
            wl.iter_rows(
                "doculect",
                "form",
                "concept",
                "cogid",
                "morphemes",
                "note",
                "protoset",
                "protoform",
                "apbm",
                "basicvocabulary"
            ),
            desc="cldfify"
        ):
            # lexeme = args.writer.add_form_with_segments(
            args.writer.add_form(
                Parameter_ID=concepts[concept.lower()],
                Language_ID=doculect,
                Form=form.strip(),
                Value=form.strip(),
                Morphemes=morphemes,
                ProtoSet=protoset,
                ProtoForm=protoform,
                APBM=apbm,
                BasicVocabulary=basicvocabulary,
                Cognacy=cogid,
                Comment=note,
                Source="Seifart2015"
            )

            # args.writer.add_cognate(
            #     lexeme=form,
            #     Cognateset_ID=cogid,
            #     Cognate_Detection_Method="expert"
            #     )
