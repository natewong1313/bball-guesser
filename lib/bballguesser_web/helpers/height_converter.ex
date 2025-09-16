defmodule HeightConverter do
  def to_feet_and_inches(total_inches) when is_integer(total_inches) and total_inches >= 0 do
    feet = div(total_inches, 12)
    inches = rem(total_inches, 12)
    {feet, inches}
  end
end
