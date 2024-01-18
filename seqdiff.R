#!/usr/bin/env Rscript
files <- c("txt/input-reproin.txt", "txt/input-orig.txt")
cols <- c("seqno","ndcm","pname")
m <- do.call(merge, c(list(by=cols[1:2],
                           suffixes=gsub('.*input-|.txt','',files)),
                    lapply(files, \(f) read.table(f,sep="\t",header=T)[,cols])))
write.table(m[order(m$seqno ),],row.names=F,sep="\t",quote=F)
