CREATE DATABASE IF NOT EXISTS Spotify.db;

CREATE TABLE IF NOT EXISTS "Playlists"(
    PlaylistID int NOT NULL,
    Name char(255) NOT NULL,
    Owner char(255) NOT NULL,
    Length int NOT NULL,
    Version int NOT NULL,
    PRIMARY KEY (PlaylistID)
);

CREATE TABLE IF NOT EXISTS "Artist"(
    ArtistID int NOT NULL,
    Name char(255) NOT NULL,
    Genre char(255) NOT NULL,
    PRIMARY KEY(ArtistID)
);

CREATE TABLE IF NOT EXISTS "Albums"(
    AblumID int NOT NULL,
    Name char(255) NOT NULL,
    ReleaseDate date NOT NULL,
    ArtistID int NOT NULL,
    PRIMARY(AlbumID),
    FOREIGN KEY (ArtistID) REFERENCES Artists(ArtistID)
);

CREATE TABLE IF NOT EXISTS "Songs"(
    SongID int NOT NULL,
    Name char(255) NOT NULL,
    Duration int NOT NULL,
    Dance float NOT NULL,
    Temp0 float NOT NULL,
    Energy float NOT NULL,
    ArtistID int NOT NULL,
    AblumID int NOT NULL,
    PlaylistID int NOT NULL,
    PRIMARY KEY(SongID),
    FOREIGN KEY (ArtistID) REFERENCES Artists(ArtistID),
    FOREIGN KEY (AlbumID) REFERENCES Albums(AlbumID),
    FOREIGN KEY (PlaylistID) REFERENCES Playlists(PlaylistID)
);