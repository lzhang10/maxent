add_library(maxent STATIC display.cpp modelfile.cpp trainer.cpp gistrainer.cpp
maxentmodel.cpp mmapfile.c lbfgs_wrapper.c lbfgs.f lbfgstrainer.cpp)

add_executable(maxent_bin maxent.cpp maxent_cmdline.c f77_dummy_main.cpp)
target_link_libraries(maxent_bin
  PRIVATE
    maxent
  PUBLIC
    Boost::timer
    Boost::chrono
  -static
  )
set_target_properties(maxent_bin PROPERTIES OUTPUT_NAME maxent)

install(TARGETS maxent_bin DESTINATION bin)
install(TARGETS maxent DESTINATION lib)
install(FILES maxentmodel.hpp itemmap.hpp meevent.hpp ext_algorithm.hpp
itemmap.tcc eventspace.hpp  eventspace.tcc
DESTINATION include/maxent)
