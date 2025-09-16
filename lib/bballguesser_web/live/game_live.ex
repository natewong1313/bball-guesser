defmodule BballguesserWeb.GameLive do
  alias Bballguesser.{Repo, Player, Team}
  use BballguesserWeb, :live_view
  import Ecto.Query
  import HeightConverter

  @initial_search_form %{"name" => ""}
  def mount(_params, _session, socket) do
    player =
      Repo.one(
        from p in Player,
          join: t in Team,
          on: p.team_name == t.name,
          order_by: fragment("RANDOM()"),
          limit: 1,
          select: %{
            name: p.name,
            positions: p.positions,
            age: p.age,
            height: p.height,
            number: p.number,
            school: p.school,
            image_url: p.image_url,
            team_name: p.team_name,
            conference: t.conference,
            division: t.division
          }
      )

    IO.puts(player.name)

    {:ok,
     assign(socket,
       hello: "world",
       player: player,
       search_form: to_form(@initial_search_form, as: "search"),
       search_results: [],
       guesses: []
     )}
  end

  def handle_params(_params, _, socket) do
    IO.puts("handle params")
    {:noreply, push_event(socket, "restoreSettings", %{key: "hello"})}
  end

  def handle_event("search", %{"name" => name}, socket) do
    IO.puts("search")
    query = from p in Player, where: ilike(p.name, ^"%#{name}%"), limit: 5

    search_results =
      if String.trim(name) != "" do
        Repo.all(query)
      else
        []
      end

    search_form = to_form(%{"name" => name}, as: "search")
    {:noreply, assign(socket, search_form: search_form, search_results: search_results)}
  end

  def handle_event("guess", %{"name" => name}, socket) do
    guessed_player =
      Repo.one(
        from p in Player,
          join: t in Team,
          on: p.team_name == t.name,
          where: p.name == ^name,
          select: %{
            name: p.name,
            positions: p.positions,
            age: p.age,
            height: p.height,
            number: p.number,
            school: p.school,
            image_url: p.image_url,
            team_name: p.team_name,
            conference: t.conference,
            division: t.division
          }
      )

    updated_guesses = socket.assigns.guesses ++ [guessed_player]

    socket =
      if guessed_player.name == socket.assigns.player.name do
        put_flash(socket, :info, "🎉 Congratulations! Reload the page to play the game again")
      else
        socket
      end

    {:noreply,
     assign(socket,
       search_form: to_form(@initial_search_form, as: "search"),
       search_results: [],
       guesses: updated_guesses
     )}
  end
end
