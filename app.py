from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from models import Artist, UUID
from typing import Final

app = FastAPI()
GENRES: Final[list[str]] = ["POP", "RAP", "R&B", "ROCK"]

artists: dict[str, Artist] = {}


def is_added(id: str) -> Artist:
    if id not in artists:
        raise HTTPException(status_code=404, detail="Artist not found!")
    return artists[id]


@app.get("/show_artists")
async def view_artists() -> dict[str, Artist]:
    return artists


@app.get("/artist/view")
async def view_artist(id: str) -> Artist:
    return is_added(id)


@app.post("/artist/add")
async def add_artist(artist: Artist) -> JSONResponse:
    if artist.music_genre.upper() not in GENRES:
        raise HTTPException(
            status_code=406,
            detail="Invalid music genre!"
        )

    artists[UUID()] = artist

    return JSONResponse(
        status_code=201,
        content=f"{artist.name} successfully added!"
    )


@app.post("/artist/add-song")
async def add_song(id: str, year_of_release: str, title: str) -> JSONResponse:
    artist = is_added(id)

    if year_of_release not in artist.releases:
        artist.releases[year_of_release] = []
    artist.releases[year_of_release].append(title)

    return JSONResponse(
        status_code=200,
        content=f"{title} successfully added!"
    )


@app.put("/artist/update")
async def update_artist(id: str, name: str = None, age: int = None, music_genre: str = None,
                        is_active: bool = True) -> JSONResponse:
    fetched_data: dict = {
        "name": name, "age": age, "music_genre": music_genre, "is_active": is_active
    }

    is_added(id).__dict__.update({
        key: value for (key, value) in fetched_data.items() if value is not None
    })

    return JSONResponse(
        status_code=200,
        content="Song successfully updated!"
    )


@app.delete("/artist/delete")
async def delete_artist(id: str) -> JSONResponse:
    if is_added(id):
        del artists[id]

        return JSONResponse(
            status_code=200,
            content="Artist successfully deleted!"
        )


@app.delete("/artist/delete-song")
async def delete_song(id: str, year_of_release: str, title: str) -> JSONResponse:
    artist = is_added(id)
    songs: list = artist.releases[year_of_release]

    if title not in songs:
        raise HTTPException(status_code=404, detail=f"{title} is not published yet!")

    # Removing the song and deleting the key if the list of songs is empty
    artist.releases[year_of_release].remove(title)
    if not artist.releases[year_of_release]:
        del artist.releases[year_of_release]

    return JSONResponse(
        status_code=200,
        content="Song successfully deleted!"
    )
