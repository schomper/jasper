cmake_minimum_required(VERSION 3.3)
project(lda_c_dist)


set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c++11")

set(SOURCE_FILES
    cokus.c
    cokus.h
    lda-alpha.c
    lda-alpha.h
    lda-data.c
    lda-data.h
    lda-estimate.c
    lda-estimate.h
    lda-inference.c
    lda-inference.h
    lda-model.c
    lda-model.h
    lda.h
    utils.c
    utils.h)

add_executable(lda_c_dist ${SOURCE_FILES})