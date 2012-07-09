interface Fn<A, B> {
  public B ap(final A a);
}

public class Currying {

  // This is our compose function
  public static <A,B,C>
    Fn<Fn<B,C>, // (b -> c) -> 
    Fn<Fn<A,B>, // (a -> b) -> 
    Fn<A,C>>>   // (a -> c)
    compose(){
    return new Fn<Fn<B,C>, 
      Fn<Fn<A,B>, 
      Fn<A,C>>> () {
      public Fn<Fn<A,B>, 
        Fn<A,C>> ap(final Fn<B,C> f){
        return new Fn<Fn<A,B>, 
          Fn<A,C>>() {
          public Fn<A,C> ap(final Fn<A,B> g){
            return new Fn<A,C>(){
              public C ap(final A a){
                return f.ap(g.ap(a));
              }
            };
          }
        };
      }
    };
  }

  // This is our add function
  public static Fn<Integer, Fn<Integer, Integer>> add(){
    return new Fn<Integer, Fn<Integer, Integer>>(){
      public Fn<Integer,Integer> ap(final Integer a) {
        return new Fn<Integer, Integer>() {
          public Integer ap(final Integer b){
            return a + b;
          }
        };
      }
    };
  }

  // This is our multiply function
  public static Fn<Integer, Fn<Integer, Integer>> mult(){
    return new Fn<Integer, Fn<Integer, Integer>>(){
      public Fn<Integer,Integer> ap(final Integer a) {
        return new Fn<Integer, Integer>() {
          public Integer ap(final Integer b){
            return a * b;
          }
        };
      }
    };
  }
  
  // This is the lessthan function
  public static Fn<Integer, Fn<Integer, Boolean>> lessthan(){
    return new Fn<Integer, Fn<Integer, Boolean>>(){
      public Fn<Integer, Boolean> ap(final Integer a){
        return new Fn<Integer, Boolean>(){
          public Boolean ap(final Integer b){
            return a < b;
          }
        };
      }
    };
  }

  // This is the string length function
  public static Fn<String, Integer> length(){
    return new Fn<String, Integer>(){
      public Integer ap(final String str){
        return str.length();
      }
    };
  }
  
  // This is a tricky one! It takes a curried function of two arguments as its
  // first argument (we'll call this function f), then it returns a new curried
  // function that takes the two arguments in reversed order! We use this in the
  // main function to flip the order of the lessthan function's arguments so we
  // can have the function that answers the question "is it less than two?",
  // rather than "is two less than it?"
  public static <A,B,C> 
    Fn<Fn<A,Fn<B,C>>, // (a -> b -> c) ->
    Fn<B,Fn<A,C>>>  // (b -> a -> c)
    flip(){
    return new Fn<Fn<A,Fn<B,C>>, Fn<B,Fn<A,C>>>(){
      public Fn<B, Fn<A,C>> ap(final Fn<A,Fn<B,C>> f){
        return new Fn<B, Fn<A,C>>(){
          public Fn<A,C> ap(final B b){
            return new Fn<A,C>(){
              public C ap(final A a){
                return f.ap(a).ap(b);
              }
            };
          }
        };
      }
    };
  }

  public static void main(String[] argv){
    // Basic usage of currying
    System.out.println(add().ap(3).ap(4));
    // Next, lets try (3 * 4) + 2
    // First lets create the (+2) function...
    Fn<Integer, Integer> plus2 = add().ap(2);
    // next, the times 3 function
    Fn<Integer, Integer> times3 = mult().ap(3);
    // now we compose them into a multiply by 2 and add 3 function
    Fn<Integer, Integer> times3plus2 = Currying.<Integer,Integer,Integer>
      compose().ap(plus2).ap(times3);
    // without compose
    System.out.println(plus2.ap(times3.ap(4)));
    // with compose
    System.out.println(times3plus2.ap(4));

    //Let's do something with different data types!

    // First lets create the "is this less than 7?" function. We have to use
    // flip to flip the order of arguments to lessthan so we get the right
    // meaning 
    Fn<Integer, Boolean> lessthan7 = Currying.<Integer,Integer,Boolean>
      flip().ap(lessthan()).ap(7);
    // Next, let's compose lessthan7 and length
    Fn<String,Boolean> lengthlessthan7 = Currying.<String,Integer,Boolean>
      compose().ap(lessthan7).ap(length());

    // Now let's use our cool function in a loop
    String[] strings = {"Hi","there","majestic","person"};
    for (String str : strings){
      System.out.println(lengthlessthan7.ap(str));
    }
  } 
}
  