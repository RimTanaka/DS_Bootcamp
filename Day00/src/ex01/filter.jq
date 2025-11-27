# filter.jq
.items[]? |
{
  id: .id,
  created_at: .created_at,
  name: .name,
  has_test: .has_test,
  alternate_url: .alternate_url
}
