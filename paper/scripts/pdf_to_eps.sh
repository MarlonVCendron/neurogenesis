if [ -z "$1" ]; then
  echo "Usage: $0 <input file>"
  exit 1
fi

if [ -z "$2" ]; then
  echo "Usage: $0 <output file>"
  exit 1
fi

# If pdffonts source.pdf shows emb=yes, use pdftops
gs -o $2 -sDEVICE=eps2write -dEmbedAllFonts=true -dSubsetFonts=true -c "<< /NeverEmbed [] >> setdistillerparams" -f $1