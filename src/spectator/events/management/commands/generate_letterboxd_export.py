import csv

from django.core.management.base import BaseCommand, CommandError

from spectator.events.models import Event


class Command(BaseCommand):
    """
    Generates a CSV file containing information about Works of kind
    "movie" that have been seen, suitable for importing into a
    Letterboxd.com account.

    Import docs: https://letterboxd.com/about/importing-data/
    """

    help = (
        "Generates a CSV file of watched movies suitable for import into Letterboxd.com"
    )

    filename = "watched_movies.csv"

    def handle(self, *args, **options):
        "This is called when the command is run."
        rows = self.make_rows()

        if len(rows) == 0:
            msg = "No movies were found."
            raise CommandError(msg)

        self.write_csv_file(rows)

        plural = "movie" if len(rows) == 1 else "movies"
        self.stdout.write(
            self.style.SUCCESS(f"Wrote {len(rows)} {plural} to {self.filename}")
        )

    def make_rows(self):
        """
        Returns a list of dicts, each one about a single viewing of
        a movie.
        """
        rows = []
        watched_work_ids = []

        for event in Event.objects.filter(kind="cinema").order_by("date"):
            for selection in event.get_movies():
                work = selection.work
                is_rewatch = work.id in watched_work_ids

                directors = []
                for role in work.roles.all():
                    if role.role_name.lower() == "director":
                        directors.append(role.creator.name)

                rows.append(
                    {
                        "imdbID": work.imdb_id,
                        "Title": work.title,
                        "Year": work.year,
                        "Directors": ", ".join(directors),
                        "WatchedDate": event.date.strftime("%Y-%m-%d"),
                        "Rewatch": str(is_rewatch).lower(),
                    }
                )

                watched_work_ids.append(work.id)

        return rows

    def write_csv_file(self, rows):
        """
        Passed a list of dicts - each one being data about single
        viewing of a movie - writes this out to a CSV file.
        """
        with open(self.filename, mode="w") as movies_file:
            writer = csv.DictWriter(
                movies_file,
                fieldnames=rows[0].keys(),
                delimiter=",",
                quotechar='"',
                quoting=csv.QUOTE_MINIMAL,
            )

            writer.writeheader()

            for row in rows:
                writer.writerow(row)
