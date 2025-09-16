defmodule Bballguesser.Repo.Migrations.CreateTeams do
  use Ecto.Migration

  def change do
    create table(:teams, primary_key: false) do
      add :name, :string, primary_key: true
      add :conference, :string
      add :division, :string
      add :logo_url, :string

      timestamps(type: :utc_datetime)
    end
  end
end
